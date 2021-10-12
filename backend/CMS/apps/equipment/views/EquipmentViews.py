from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.db import transaction
from CMS.apps.equipment.serializers import equipmentSerializers, NeTypeSerializers, statusSerializers
from CMS.apps.equipment.models import Networkequipment, NeType, Nestatus, NestatusType
from rest_framework.pagination import PageNumberPagination


class StandardPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100


class EquipmentView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = equipmentSerializers
    queryset = Networkequipment.objects.all()
    pagination_class = StandardPageNumberPagination
    filter_fields = ('ip', 'name', 'type')

    def post(self, request, *args, **kwargs):
        ip = request.data.get('ip')
        try:
            Networkequipment.objects.get(ip=ip)
        except Exception as e:
            if isinstance(e, Networkequipment.DoesNotExist):
                return self.create(request, *args, **kwargs)
            else:
                return Response({'msg': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'IP地址不能重复。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_destroy(self, instance):
        if instance.user is None:
            instance.delete()
        else:
            # 删除设备的用户
            with transaction.atomic():
                # 创建事务保存点
                save_point = transaction.savepoint()
                try:
                    user = instance.user
                    instance.user = None
                    user.delete()
                    instance.delete()
                except Exception as e:
                    print(e)
                    transaction.savepoint_rollback(save_point)
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NeTypeView(RetrieveUpdateDestroyAPIView, ListCreateAPIView):
    serializer_class = NeTypeSerializers
    queryset = NeType.objects.all()


class StatusView(RetrieveUpdateDestroyAPIView, ListCreateAPIView):
    serializer_class = statusSerializers
    queryset = Nestatus.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # 更新状态类型
        type_id = request.data.get('type_id')
        type = NestatusType.objects.get(id=type_id)
        instance.type = type
        instance.save()

        return Response(serializer.data)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            save_id = transaction.savepoint()
            ne_id = request.data.get('id')
            data = request.data.get('status')
            try:
                # 1. 创建状态对象
                status_ins = Nestatus.objects.create(date=data.get('date'),
                                                     site=data.get('site'),
                                                     remark=data.get('remark'),
                                                     type_id=data.get('type_id')
                                                     )
                # 2. 关联
                equipment = Networkequipment.objects.get(id=ne_id)
                equipment.status = status_ins
                equipment.save()
            except Exception as e:
                print(e)
                transaction.savepoint_rollback(save_id)
                return Response({
                    'code': 500,
                    'errmsg': '创建设备状态失败'
                })
            serializer = self.serializer_class(status_ins)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class EquipmentByIpView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        # print(request.query_params)
        beginIP = request.query_params.get('beginIP')
        endIP = request.query_params.get('endIP')
        vendor = request.query_params.get('vendor')
        print(beginIP, endIP)
        # < QueryDict: {'beginIP': ['1'], 'endIP': ['1'], 'vendor': ['huawei']} >
        # 给个思路：
        # 在validator里面先判断是否合法ip，用正则([1 - 9] | [1 - 9]\\d | 1\\d
        # {2} | 2[0 - 4]\\d | 25[0 - 5])(\\.(\\d |[1-9]\\d | 1\\d{2} | 2[0-4]\\d | 25[0-5])){3}
        #
        # 然后比较
        # "192.168.100.1" <= ipStr <= 192.168.100.100
        # '192.168.0.1' <= '192.168.0.100'
        # True
        equipments = Networkequipment.objects.all()
        try:

            if beginIP != '':
                equipments = equipments.filter(ip__gte=beginIP)
            if endIP != '':
                equipments = equipments.filter(ip__lte=endIP)
            if vendor != '':
                equipments = equipments.filter(vendor__device_param=vendor)

        except Exception as e:
            print(e)
            Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(equipments)
        serializers = equipmentSerializers(equipments, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
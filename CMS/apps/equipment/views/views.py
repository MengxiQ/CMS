from django.db.models import Max
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response

from CMS.apps.equipment.serializers import equipmentSerializers, NeTypeSerializers, statusSerializers, NetconfUsersSerializer
from CMS.apps.equipment.models import Networkequipment, NeType, Nestatus, NestatusType, NetconfUsers

from rest_framework.pagination import PageNumberPagination


class StandardPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100


class Equipment(UpdateModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericAPIView,):
    serializer_class = equipmentSerializers
    queryset = Networkequipment.objects.all()
    pagination_class = StandardPageNumberPagination
    filter_fields = ('ip', 'name', 'type')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, pk):
        return self.list(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        networkequipment = self.perform_create(serializer)

        # 关联设备类型
        print(request.data)
        type = NeType.objects.get(tid=request.data.get('type'))
        # networkequipment = Networkequipment.objects.get(neid=serializer.data.get('neid'))
        networkequipment.type = type
        networkequipment.save()

        # 创建netconf账户
        netconfUserData = request.data.get('netconfUser')
        netconfUserSerializer = NetconfUsersSerializer(data=netconfUserData)
        netconfUserSerializer.is_valid(raise_exception=False)
        netconfUser = netconfUserSerializer.save()
        netconfUser.equipment = networkequipment
        netconfUser.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, pk):
        return self.create(request)


class NeTypeView(ListModelMixin, GenericAPIView,):
    serializer_class = NeTypeSerializers
    queryset = NeType.objects.all()

    def get(self, request):
        return self.list(request)


class StatusView(GenericAPIView, CreateModelMixin, UpdateModelMixin):
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
        type = NestatusType.objects.get(tid=request.data.get('type'))
        instance.type = type
        instance.save()

        return Response(serializer.data)

    def put(self, request, pk):
        return self.update(request)

    def create(self, request, *args, **kwargs):
        status = request.data.get('status')
        # id 查询最大的+1
        max_id = Nestatus.objects.aggregate(Max('id')).get('id__max')
        # Nestatus表为空则返回None，如果为None则设置为0
        if(max_id == None):
            max_id = 0
        # 查询type
        type = NestatusType.objects.get(tid=status.get('type'))
        new_status = Nestatus.objects.create(date=status.get('date'),
                                             site=status.get('site'),
                                             remark=status.get('remark'),
                                             id=int(max_id)+1,
                                             type=type
                                             )
        # new_status 为 0 需要重新设置
        new_status.id = int(max_id)+1
        serializer = self.serializer_class(new_status)

        # 关联
        neid = request.data.get('neid')
        networkequipment = Networkequipment.objects.get(neid=neid)

        networkequipment.status = new_status
        networkequipment.save()


        return Response(serializer.data)

    def post(self, request, pk):
        return self.create(request)
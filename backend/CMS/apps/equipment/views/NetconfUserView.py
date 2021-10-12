from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from CMS.apps.equipment.models import NetconfUsers, Networkequipment
from CMS.apps.equipment.serializers import NetconfUsersSerializer
from django.db import transaction


class NetconfUserView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = NetconfUsers.objects.all()
    serializer_class = NetconfUsersSerializer
    # filter_fields = ('username', 'device_params')

    def put(self, request, *args, **kwargs):
        ip = request.data.get('networkequipment')
        try:
            Networkequipment.objects.get(ip=ip)
        except Exception as e:
            print(e)
            if not (ip == '' or ip is None):
                return Response({'msg': '该IP地址的设备不存在！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return self.update(request, *args, **kwargs)


class BatchUsers(GenericAPIView):
    def post(self, request, *args, **kwargs):
        # print(request.data)
        equipmentsIdList = request.data.get('equipmentsIdList')
        choicUser = request.data.get('choicUser')
        with transaction.atomic():
            save_point = transaction.savepoint()
            try:
                # 1.查询出所有的设备
                equipments = Networkequipment.objects.filter(id__in=equipmentsIdList)
                # 2.遍历查出的设备添加用户
                for item in equipments:
                    # 判断是否已有用户
                    # netconfusers_set = item.netconfusers_set.all()
                    # if (len(netconfusers_set) == 0):
                    if item.user is None:
                        # 没有用户，则创建用户
                        user = NetconfUsers.objects.create(username=choicUser.get('username'),
                                                           password=choicUser.get('password'),
                                                           port=choicUser.get('port'),
                                                           device_params=choicUser.get('device_params'))
                        # 绑定用户
                        item.user = user
                        item.save()
                    else:
                        # 已有用户，则更新用户
                        item.user.username = choicUser.get('username')
                        item.user.password = choicUser.get('password')
                        item.user.port = choicUser.get('port')
                        item.user.device_params = choicUser.get('device_params')
                        item.save()

            except Exception as e:
                print(e)
                transaction.rollback(save_point)
                return Response({'msg': '批量失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': '批量成功'}, status=status.HTTP_201_CREATED)

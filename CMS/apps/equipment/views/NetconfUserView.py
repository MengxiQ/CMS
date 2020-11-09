from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from CMS.apps.equipment.models import NetconfUsers, Networkequipment
from CMS.apps.equipment.serializers import NetconfUsersSerializer
from django.db import transaction


class NetconfUserView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = NetconfUsers.objects.all()
    serializer_class = NetconfUsersSerializer
    filter_fields = ('username', 'device_params')

    def getUserbyIp(self, ip):
        instance = self.queryset.filter(equipment__ip=ip)
        serializer = self.serializer_class(instance[0])
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        ip = request.query_params.get('ip')
        if ip:
            return self.getUserbyIp(ip)
        return self.list(request)
    #
    # def post(self, request, pk):
    #     return self.create(request)
    #
    # def put(self, request, pk):
    #     return self.update(request)
    #
    # def delete(self, request, pk):
    #     return self.delete(request)


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
                    netconfusers_set = item.netconfusers_set.all()
                    if (len(netconfusers_set) == 0):
                        # 没有用户，则创建用户
                        user = NetconfUsers.objects.create(username=choicUser.get('username'),
                                                           password=choicUser.get('password'),
                                                           port=choicUser.get('port'),
                                                           device_params=choicUser.get('device_params'))
                        # 绑定用户
                        user.equipment = item
                        user.save()
                    else:
                        # 已有用户，则更新用户
                        item.netconfusers_set.update(username=choicUser.get('username'),
                                                     password=choicUser.get('password'),
                                                     port=choicUser.get('port'),
                                                     device_params=choicUser.get('device_params'))

            except Exception as e:
                print(e)
                transaction.rollback(save_point)
                return Response({'msg': '批量失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': '批量成功'}, status=status.HTTP_201_CREATED)

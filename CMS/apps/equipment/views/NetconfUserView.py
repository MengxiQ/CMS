from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, \
    RetrieveModelMixin
from rest_framework.response import Response
from CMS.apps.equipment.models import NetconfUsers
from CMS.apps.equipment.serializers import NetconfUsersSerializer


class NetconfUserView(GenericAPIView,
                      ListModelMixin,
                      CreateModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,):
    queryset = NetconfUsers.objects.all()
    serializer_class = NetconfUsersSerializer

    def getUserbyIp(self, ip):
        instance = self.queryset.filter(equipment__ip=ip)
        serializer = self.serializer_class(instance[0])
        return  Response(serializer.data)


    def get(self, request, pk):
        ip = request.query_params.get('ip')
        if ip:
            return self.getUserbyIp(ip)
        return self.list(request)



    def post(self, request, pk):
        return self.create(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.delete(request)

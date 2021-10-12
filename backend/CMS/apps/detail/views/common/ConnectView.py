from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from CMS.apps.detail.views.Generics.GetUserInfo import GetUserInfo
from CMS.apps.detail.views.Generics.Connector import Connector


class ConnectView(GenericAPIView, GetUserInfo, Connector):

    def get(self, request, *args, **kwargs):
        ip = request.query_params.get('ip')
        user, template_xml_string, params, position = self.getInfo(ip=ip)
        m = self.connect(ip=ip, user=user)
        if m._session.connected:
            return Response({'msg': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': '连接[' + ip + ']失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        ip = request.data.get('ip')
        flag = self.disconnect(ip=ip)
        if flag:
            return Response({'msg': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': '关闭连接[' + ip + ']失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
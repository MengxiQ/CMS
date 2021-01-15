from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from CMS.apps.detail.views.Generics.Connector import Connector
from CMS.apps.detail.views.Generics.GetUserInfo import GetUserInfo


class MaintainView(GenericAPIView, GetUserInfo, Connector):
    def post(self, request, *args, **kwargs):
        return self.saveConfig(request, *args, **kwargs)

    def saveConfig(self, request, *args, **kwargs):
        ip = request.data.get('ip')
        source = request.data.get('source')
        target = request.data.get('target')
        try:
            user, template_xml_string, params = self.getInfo(ip=ip)
            m = self.connect(ip, user)
            result = m.copy_config(source=source, target=target)
        except Exception as e:
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)
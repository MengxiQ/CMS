from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from CMS.apps.tools.testTools import ping_text


class PingTestView(GenericAPIView):

    # ping 设备ip地址
    def get(self, request, pk):
        ip = request.query_params.get('ip')
        res = ping_text(ip, 4)
        return Response({'data': res}, status=status.HTTP_200_OK)

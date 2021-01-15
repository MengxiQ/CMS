from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from CMS.apps.detail.views.Generics.ConfigMangeGenerics import ConfigMangeGenerics


class CommitView(GenericAPIView, ConfigMangeGenerics):

    def post(self, request):
        ip = request.data.get('ip')
        options = request.data.get('options')
        try:
            self.commit(ip, options)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)

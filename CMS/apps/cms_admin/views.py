from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from CMS.apps.cms_admin.serializers import userSerializers
import jwt

class userView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = userSerializers

    def get(self, request):
        token = request.query_params['token']
        decode_token = jwt.decode(token, key=api_settings.JWT_SECRET_KEY, algorithms=api_settings.JWT_ALGORITHM)
        user = self.queryset.get(username=decode_token['username'])
        data = self.get_serializer(user).data
        data['avatar'] = 'admin'
        data['code'] = 20000
        return Response(data)
        # return self.retrieve(request)
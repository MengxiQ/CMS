from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from CMS.apps.cms_admin.serializers import userSerializers
import jwt


class userView(GenericAPIView):
    # 刷新页面重新获取用户信息
    queryset = User.objects.all()
    serializer_class = userSerializers

    def get(self, request):
        token = request.query_params['token']
        decode_token = jwt.decode(token, key=api_settings.JWT_SECRET_KEY, algorithms=api_settings.JWT_ALGORITHM)
        user = self.queryset.get(username=decode_token['username'])  # 获取该用户的表信息
        data = self.get_serializer(user).data
        data['avatar'] = 'superuser' if user.is_superuser else 'admin'
        # data['code'] = 20000
        return Response(data)


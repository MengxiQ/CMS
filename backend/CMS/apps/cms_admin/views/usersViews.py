from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import User
from CMS.apps.cms_admin.serializers import usersSerializers


class usersView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = usersSerializers

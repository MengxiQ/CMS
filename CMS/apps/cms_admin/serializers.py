from rest_framework import serializers
from django.contrib.auth.models import User

class userSerializers(serializers.ModelSerializer):
    # id = serializers.p
    # username = serializers.CharField(label='username', required=False)
    # email = serializers.CharField(label='email', required=False)
    # avatar = serializers.CharField(label='权限')
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
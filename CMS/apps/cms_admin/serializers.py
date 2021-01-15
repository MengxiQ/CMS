# from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from django.contrib.auth.models import User


class userSerializers(serializers.ModelSerializer):
    # 这个是刷新页面的，不要返回密码
    # id = serializers.p
    # username = serializers.CharField(label='username', required=False)
    # email = serializers.CharField(label='email', required=False)
    # avatar = serializers.CharField(label='权限')
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class usersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    extra_kwargs = {
        'password': {
            'write_only': True,
        }
    }

    # 重写父类方法，增加管理员权限属性
    def create(self, validated_data):
        # 添加管理员字段
        validated_data['is_staff'] = True
        validated_data['is_superuser'] = True
        # 调用父类方法创建管理员用户
        admin = super().create(validated_data)
        # 用户密码加密
        password = validated_data['password']
        admin.set_password(password)
        admin.save()

        return admin

    def update(self, instance, validated_data):
        # print(validated_data)
        # password = make_password(validated_data.get('password', instance.password))
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password')
        if password is None or password == '':
            # 如果密码为空则不修改密码
            pass
        else:
            instance.set_password(password)  # 对密码进行加密处理
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.email = validated_data.get('email', instance.email)
        instance.save()  # 注意要保存数据到数据库
        return instance
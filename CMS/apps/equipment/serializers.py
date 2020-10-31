from rest_framework import serializers
from rest_framework.utils import json

from CMS.apps.equipment.models import Networkequipment, Nestatus, NestatusType, NeType, NetconfUsers


class statusTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = NestatusType
        fields = '__all__'

    def __str__(self):
        return self


class statusSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = statusTypeSerializers(many=False, read_only=True)
    type_id = serializers.IntegerField(write_only=True)
    date = serializers.DateTimeField(label='date')
    site = serializers.CharField(label='site', allow_blank=True)

    def __str__(self):
        return self.id

    def create(self, validated_data):
        return Nestatus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.type_id = validated_data.get('type_id', instance.type_id)
        instance.name = validated_data.get('date', instance.date)
        instance.site = validated_data.get('site', instance.site)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.save()  # 注意要保存数据到数据库
        return instance


class NetconfUsersSerializer(serializers.ModelSerializer):
    equipment = serializers.SlugRelatedField(slug_field='ip', label='设备IP', read_only=True)

    class Meta:
        model = NetconfUsers
        fields = '__all__'

    def create(self, validated_data):
        return NetconfUsers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.port = validated_data.get('port', instance.port)
        instance.device_params = validated_data.get('device_params', instance.device_params)
        instance.hostkey = validated_data.get('hostkey', instance.hostkey)
        instance.save()  # 注意要保存数据到数据库
        return instance


class equipmentSerializers(serializers.Serializer):
    id = serializers.IntegerField(label='id', read_only=True)
    ip = serializers.CharField(label='ip')
    name = serializers.CharField(label='name')
    mac = serializers.CharField(label='mac')
    stock_date = serializers.DateTimeField(label='stock_date')
    unittype = serializers.SlugRelatedField(slug_field='name', label='设备型号', read_only=True)
    remark = serializers.CharField(label='备注')
    verdor = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # 设备类型
    type = serializers.SlugRelatedField(label='设备类型', slug_field='name', read_only=True)
    # 设备状态
    status = statusSerializers(label='设备状态', read_only=True, many=False)
    # 设备关联的用户，从父表拿字表的信息
    # netconfusers_set = serializers.StringRelatedField(label='用户信息', read_only=True, many=True)
    netconfusers_set = NetconfUsersSerializer(label='用户信息', read_only=True, many=True)

    def create(self, validated_data):
        return Networkequipment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.ip = validated_data.get('ip', instance.ip)
        instance.name = validated_data.get('name', instance.name)
        instance.mac = validated_data.get('mac', instance.mac)
        instance.stock_date = validated_data.get('stock_date', instance.stock_date)
        instance.unittype = validated_data.get('unittype', instance.unittype)
        instance.save()  # 注意要保存数据到数据库
        return instance


class NeTypeSerializers(serializers.ModelSerializer):

    class Meta:
        model = NeType
        fields = '__all__'

    def __str__(self):
        return self



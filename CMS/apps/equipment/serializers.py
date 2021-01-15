from rest_framework import serializers
from CMS.apps.equipment.models import Networkequipment, UnitType, Nestatus, NestatusType, NeType, NetconfUsers
from CMS.apps.typesManage.serializers.TypeSerializers import UnitTypeSerializers, NeTypeSerializers


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
    # 模型类的__str__方法
    networkequipment = serializers.CharField(write_only=True, allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = NetconfUsers
        fields = '__all__'

    # 自定义networkequipment字段的验证, 将IP地址字符串转化层networkequipment对象返回给验证系统验证
    # 因为报错： Cannot assign "'192.168.100.102'": "NetconfUsers.networkequipment" must be a "Networkequipment"
    def validate_networkequipment(self, data):
        ip = data
        if ip == '' or ip is None:
            return None
        else:
            # IP地址不为空
            try:
                networkequipment = Networkequipment.objects.get(ip=ip)
                return networkequipment
            except Exception as e:
                if isinstance(e, Networkequipment.DoesNotExist):
                    print('IP地址为' + ip + '不存在。', e)
                    pass
                else:
                    print(e)

    def to_representation(self, instance):
        ret = super(NetconfUsersSerializer, self).to_representation(instance)
        ip = None
        try:
            networkequipment = Networkequipment.objects.get(user_id=instance.id)
            ip = networkequipment.ip
        except Exception as e:
            # print(e)
            pass
        ret['networkequipment'] = ip
        return ret

    def create(self, validated_data):
        user = NetconfUsers.objects.create(**validated_data)
        # print(user)
        try:
            # 如果是输入了设备的ip地址
            ip = validated_data.get('networkequipment')
            networkequipment = Networkequipment.objects.get(ip=ip)
            networkequipment.user = user
            networkequipment.save()
        except Exception as e:
            print('设备关联失败', e)
        return user

    def update(self, instance, validated_data):
        networkequipment = validated_data.get('networkequipment')
        if networkequipment is not None:
            networkequipment.user = instance
        else:
            networkequipment.user = None
        # print(validated_data)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.port = validated_data.get('port', instance.port)
        instance.device_params = validated_data.get('device_params', instance.device_params)
        instance.save()  # 注意要保存数据到数据库
        # # 关联设备
        # try:
        #     networkequipment = Networkequipment.objects.get(user_id=instance.id)  # 用户旧的关联设备
        #     networkequipment.user = validated_data.get('networkequipment', instance.networkequipment)
        #     networkequipment.save()
        # except Exception as e:
        #     if isinstance(e, Networkequipment.DoesNotExist):
        #         print('用户没有旧的关联设备', e)
        return instance


class equipmentSerializers(serializers.Serializer):
    id = serializers.IntegerField(label='id', read_only=True)
    ip = serializers.CharField(label='ip')
    name = serializers.CharField(label='name')
    stock_date = serializers.DateTimeField(label='stock_date')
    unittype = serializers.PrimaryKeyRelatedField(queryset=UnitType.objects.all())
    type = serializers.PrimaryKeyRelatedField(label='设备类型', queryset=NeType.objects.all())
    status = statusSerializers(label='设备状态', read_only=True, many=False)
    remark = serializers.CharField(label='备注', allow_blank=True, allow_null=True)
    user = NetconfUsersSerializer(label='用户信息', read_only=True, many=False)

    def __str__(self):
        return self.ip

    def to_representation(self, instance):
        type = instance.type
        unittype = instance.unittype
        ret = super(equipmentSerializers, self).to_representation(instance)
        ret['type'] = NeTypeSerializers(type).data
        ret['unittype'] = UnitTypeSerializers(unittype).data
        return ret

    def create(self, validated_data):
        return Networkequipment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print('update', validated_data)
        # 'unittype': <UnitType: UnitType object (6)>, 'type': <NeType: NeType object (1)>,
        instance.ip = validated_data.get('ip', instance.ip)
        instance.name = validated_data.get('name', instance.name)
        instance.unittype = validated_data.get('unittype', instance.unittype)
        instance.type = validated_data.get('type', instance.type)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.save()  # 注意要保存数据到数据库
        return instance




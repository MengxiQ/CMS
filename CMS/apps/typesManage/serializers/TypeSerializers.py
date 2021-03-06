from rest_framework import serializers
from CMS.apps.configManage.models import Templates, Params, TempType, Function
from CMS.apps.equipment.models import UnitType, Vendor, NeType


class BaseSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(allow_null=True)
    remark = serializers.CharField(allow_null=True)


class NeTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = NeType
        fields = '__all__'

    def __str__(self):
        return self


class VendorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class TempTypesSeralizers(BaseSerializers):

    def create(self, validated_data):
        return TempType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.save()  # 注意要保存数据到数据库
        return instance


class UnitTypeSerializers(BaseSerializers):
    # vendor = serializers.SlugRelatedField(slug_field='name', read_only=True)
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

    def to_representation(self, instance):
        vendor = instance.vendor
        ret = super(UnitTypeSerializers, self).to_representation(instance)
        ret['vendor'] = VendorSerializers(vendor).data.get('name', None)
        return ret

    def create(self, validated_data):
        print(validated_data)
        return UnitType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.save()  # 注意要保存数据到数据库
        return instance


class FunctionSerializers(BaseSerializers):

    def create(self, validated_data):
        return Function.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.save()  # 注意要保存数据到数据库
        return instance


class ParamsSerializers(serializers.ModelSerializer):
    # constraint = serializers.CharField(allow_null=True, allow_blank=True)
    class Meta:
        model = Params
        fields = '__all__'

    def create(self, validated_data):
        Params.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.label = validated_data.get('label', instance.label)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.remark = validated_data.get('role', instance.role)
        instance.save()  # 注意要保存数据到数据库
        return instance


class TemplatesSerializers(BaseSerializers):
    id = serializers.CharField(read_only=True)
    tempType = TempTypesSeralizers(allow_null=True, read_only=True)
    support = serializers.SlugRelatedField(slug_field='name', many=True, required=False, read_only=True)
    templateData = serializers.CharField(allow_null=True)  # 模板文件比较大，所以应该异步加载
    updateDate = serializers.DateTimeField(allow_null=True)
    function = FunctionSerializers(allow_null=True, read_only=True)
    position = serializers.CharField(allow_null=True)
    params_set = ParamsSerializers(allow_null=True, many=True, read_only=True)

    def create(self, validated_data):
        return Templates.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
        instance.name = validated_data.get('name', instance.name)
        # instance.tempType = validated_data.get('tempType', instance.tempType)
        # instance.unitTypes = validated_data.get('unitTypes', instance.unitTypes)
        instance.templateData = validated_data.get('templateData', instance.templateData)
        instance.updateDate = validated_data.get('updateDate', instance.updateDate)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.save()  # 注意要保存数据到数据库
        return instance

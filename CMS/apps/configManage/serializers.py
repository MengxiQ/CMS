from rest_framework import serializers
from .models import Templates, Params, TempType, Function
from CMS.apps.equipment.models import UnitType, Vendor


class BaseSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(allow_null=True)
    remark = serializers.CharField(allow_null=True)


class TempTypesSeralizers(BaseSerializers):

    def create(self, validated_data):
        return TempType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.save()  # 注意要保存数据到数据库
        return instance


class UnitTypeSerializers(BaseSerializers):
    vendor = serializers.SlugRelatedField(slug_field='name', read_only=True)

    def create(self, validated_data):
        return UnitType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.remark = validated_data.get('remark', instance.remark)
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


class ParamsSerializers(BaseSerializers):
    constraint = serializers.CharField(allow_null=True, allow_blank=True)

    def create(self, validated_data):
        Params.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.remark = validated_data.get('remark', instance.remark)
        instance.save()  # 注意要保存数据到数据库
        return instance


class TemplatesSerializers(BaseSerializers):
    id = serializers.CharField(read_only=True)
    tempType = TempTypesSeralizers(allow_null=True, read_only=True)
    support = serializers.SlugRelatedField(slug_field='name', many=True, required=False, read_only=True)
    templateData = serializers.CharField(allow_null=True)  # 模板文件比较大，所以应该异步加载
    updateDate = serializers.DateTimeField(allow_null=True)
    function = FunctionSerializers(allow_null=True, read_only=True)
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

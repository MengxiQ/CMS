from rest_framework import serializers
from CMS.apps.viewsManage.models import Topology


class TopologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Topology
        fields = '__all__'

    def create(self, validated_data):
        return Topology.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.nodes = validated_data.get('nodes', instance.nodes)
        instance.connectors = validated_data.get('connectors', instance.connectors)
        instance.save()  # 注意要保存数据到数据库
        return instance
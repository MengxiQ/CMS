from rest_framework import serializers

from CMS.apps.detail.models import Interfaces


class InterfacesSerializers(serializers.Serializer):
    ifName = serializers.CharField(allow_null=True)
    baseConfig = serializers.CharField(allow_null=True)
    ipv4Config = serializers.CharField(allow_null=True)
    ipv6Config = serializers.CharField(allow_null=True)
    equipment = serializers.SlugRelatedField(slug_field='ip', label='设备IP', read_only=True)

    def create(self, validated_data):
        return Interfaces.objects.create(**validated_data)


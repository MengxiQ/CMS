import json

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from CMS.apps.viewsManage.models import Topology
from CMS.apps.equipment.models import NestatusType
from CMS.apps.viewsManage.serializers import TopologySerializer


class TopologyView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = TopologySerializer
    queryset = Topology.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        for item in queryset:
            nodes = json.loads(item.nodes)  # 这个是数据对象
            for key in range(len(nodes)):
                # 拿ip去查设备的状态
                ip = nodes[key].get('ip')
                statusType = NestatusType.objects.get(nestatus__networkequipment__ip=ip)
                nodes[key]['status'] = statusType.name
            item.nodes = json.dumps(nodes)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
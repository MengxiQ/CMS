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
            nodes = json.loads(item.nodes)  # 节点对象列表
            for key in range(len(nodes)):
                # 拿ip去查设备的状态
                ip = nodes[key].get('ip')
                try:
                    # 当更改了设备的列表的地址后拓扑这边没更新过来，会使得过滤不到对象
                    # 所以这时不更新状态
                    statusType = NestatusType.objects.get(nestatus__networkequipment__ip=ip)
                    nodes[key]['status'] = statusType.name
                except Exception as e:
                    print(e)
            item.nodes = json.dumps(nodes)

            connectors = json.loads(item.connectors)
            for key in range(len(connectors)):
                # 拿ip去查设备的状态
                dip = connectors[key].get('targetNode').get('ip')
                sip = connectors[key].get('sourceNode').get('ip')
                try:
                    # 当更改了设备的列表的地址后拓扑这边没更新过来，会使得过滤不到对象
                    # 所以这时不更新状态
                    d_statusType = NestatusType.objects.get(nestatus__networkequipment__ip=dip)
                    s_statusType = NestatusType.objects.get(nestatus__networkequipment__ip=sip)
                    if d_statusType.name == s_statusType.name and s_statusType.name == '在线':
                        connectors[key]['status'] = '在线'
                    else:
                        connectors[key]['status'] = '离线'
                    # print(connectors[key]['status'])
                except Exception as e:
                    print(e)
            item.connectors = json.dumps(connectors)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
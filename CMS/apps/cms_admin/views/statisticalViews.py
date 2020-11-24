from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from CMS.apps.equipment.models import Networkequipment
from CMS.apps.configManage.models import Templates, Function
from CMS.apps.viewsManage.models import Topology


class StatisticalViews(GenericAPIView):

    def get(self,request):
        try:
            data = {
                # 拥有设备数量
                'equipments': Networkequipment.objects.count(),
                # 模板数量
                'templates': Templates.objects.count(),
                # 功能数量
                'functions': Function.objects.count(),
                # 视图数量
                'topologys': Topology.objects.count()
            }
        except Exception as e:
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'data': data}, status=status.HTTP_200_OK)
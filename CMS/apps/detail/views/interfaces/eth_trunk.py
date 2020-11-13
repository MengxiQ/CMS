from rest_framework import status
from rest_framework.response import Response

from CMS.apps.configManage.serializers import ParamsSerializers
from CMS.apps.tools.configTools import edit_config, getInfo
from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class EthTrunkView(ConfigAPIVies):
    functionName = '配置Eth-Trunk'


class TrunkMemberView(ConfigAPIVies):
    functionName = '配置Eth-Trunk成员接口'

    def list(self, request, *args, **kwargs):
        """
        获取返回配置列表，并返回配置参数列表
        """

        ip = request.query_params.get('ip')
        try:
            # 1. 根据ip查到设备信息：netconf user信息, 模板信息
            user, template_xml_string, params = getInfo(ip=ip, functionName=self.functionName)
            paramsList = []
            for item in params:
                paramsSerializers = ParamsSerializers(item)
                paramsList.append(paramsSerializers.data)
        except Exception as e:
            print(e)
            return Response({'msg': '获取TrunkMember参数失败！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': '', 'params': paramsList},
                        status=status.HTTP_200_OK)

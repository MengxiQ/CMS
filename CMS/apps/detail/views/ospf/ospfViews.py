from xml.dom.minidom import parseString

from rest_framework import status
from rest_framework.response import Response

from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies
from CMS.apps.detail.tools import getInfo
from CMS.apps.configManage.serializers import ParamsSerializers


class OspfViews(ConfigAPIVies):
    functionName = '获取ospf信息'  # 必要，配置模板的名称


class OspfProcessView(ConfigAPIVies):
    functionName = '配置ospfv2进程'

    def list(self, request, *args, **kwargs):
        """
        并返回配置参数列表
        """
        ip = request.query_params.get('ip')
        try:
            # 1. 根据ip查到设备信息：netconf user信息, 模板信息
            user, template_xml_string, params = getInfo(ip=ip, functionName=self.functionName)

            # 2. 获取get-template元素的内容
            try:
                domTree = parseString(template_xml_string)
                template_get_xml = domTree.getElementsByTagName(self.get_TagName)[0].childNodes[1].toxml()
            except Exception as e:
                print(e)
                return Response({'msg': 'XML模板错误！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            paramsList = []
            for item in params:
                paramsSerializers = ParamsSerializers(item)
                paramsList.append(paramsSerializers.data)

        except Exception as e:
            print(e)
            return Response({'msg': '获取模板失败！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': '', 'params': paramsList}, status=status.HTTP_200_OK)


class OspfAreaView(ConfigAPIVies):
    functionName = '配置ospfv2区域'

    def list(self, request, *args, **kwargs):
        """
        并返回配置参数列表
        """
        ip = request.query_params.get('ip')
        try:
            # 1. 根据ip查到设备信息：netconf user信息, 模板信息
            user, template_xml_string, params = getInfo(ip=ip, functionName=self.functionName)

            # 2. 获取get-template元素的内容
            try:
                domTree = parseString(template_xml_string)
                template_get_xml = domTree.getElementsByTagName(self.get_TagName)[0].childNodes[1].toxml()
            except Exception as e:
                print(e)
                return Response({'msg': 'XML模板错误！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            paramsList = []
            for item in params:
                paramsSerializers = ParamsSerializers(item)
                paramsList.append(paramsSerializers.data)

        except Exception as e:
            print(e)
            return Response({'msg': '获取模板失败！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': '', 'params': paramsList}, status=status.HTTP_200_OK)


class OspfAreaNetwork(ConfigAPIVies):
    functionName = '配置ospf区域网络'

    def list(self, request, *args, **kwargs):
        """
        并返回配置参数列表
        """
        ip = request.query_params.get('ip')
        try:
            # 1. 根据ip查到设备信息：netconf user信息, 模板信息
            user, template_xml_string, params = getInfo(ip=ip, functionName=self.functionName)

            # 2. 获取get-template元素的内容
            try:
                domTree = parseString(template_xml_string)
                template_get_xml = domTree.getElementsByTagName(self.get_TagName)[0].childNodes[1].toxml()
            except Exception as e:
                print(e)
                return Response({'msg': 'XML模板错误！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            paramsList = []
            for item in params:
                paramsSerializers = ParamsSerializers(item)
                paramsList.append(paramsSerializers.data)

        except Exception as e:
            print(e)
            return Response({'msg': '获取模板失败！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': '', 'params': paramsList}, status=status.HTTP_200_OK)


class OspfAdvanceView(ConfigAPIVies):
    functionName = '配置ospf高级配置'

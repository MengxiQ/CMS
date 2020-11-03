import json

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from CMS.apps.equipment.models import UnitType, Networkequipment, NetconfUsers
from CMS.apps.configManage.serializers import TemplatesSerializers, ParamsSerializers
from CMS.apps.configManage.models import Templates
from ncclient import manager
from xml.dom.minidom import parse, parseString
import xmltodict
from string import Template


class VlansViews(GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        获取vlan列表，并返回配置参数（）
        """
        # 1. 根据ip查到设备信息：厂商参数，netconf信息,设备型号
        ip = request.query_params.get('ip')
        equipment = Networkequipment.objects.get(ip=ip)
        user = NetconfUsers.objects.filter(equipment=equipment)[0]
        unniType = UnitType.objects.filter(networkequipment__ip=ip)[0]

        # 2. 查询支持的模板 和模板类型
        try:
            template = unniType.templates_set.all().filter(tempType__name='VLAN配置模板')[0]
            serializers = TemplatesSerializers(template)

            # 3. 获取到配置模板
            template_xml_string = serializers.data.get('templateData')

            # 4. 获取get-template元素的内容
            domTree = parseString(template_xml_string)
            template_get_xml = domTree.getElementsByTagName('tempalte-get')[0].childNodes[1].toxml()

            # 5，获取配置参数列表
            params = template.params_set.all()
            paramsList = []
            for item in params:
                paramsSerializers = ParamsSerializers(item)
                paramsList.append(paramsSerializers.data)

        except Exception as e:
            print(e)
            return Response({'msg': '获取模板失败！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # 5.使用设备用户连接设备

            connect = manager.connect(host=ip, port=user.port, username=user.username,
                                      password=user.password, hostkey_verify=False,
                                      device_params={'name': user.device_params},
                                      allow_agent=False, look_for_keys=False)

            with connect as m:
                reply_obj = m.get_config(source='running', filter=template_get_xml)
                reply_json_data = xmltodict.parse(str(reply_obj))
                # print(reply_json_data)
        except Exception as e:
            print(e)
            Response({'msg': '连接设备或者下发配置出错！', 'erro': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'vlans': reply_json_data['rpc-reply']['data']['vlan']['vlans']['vlan'], 'params': paramsList},
                        status=status.HTTP_200_OK)

    def getInfo(self, ip):
        """
        获取设备相关信息
        :param ip: 设备的IP地址
        :return: 返回的是一个字典
        {
        user：netconf账户（model object）
        template_xml_string：string形式的配置模板信息（string）
        params: 参数列表（Questet List）
        }
        """
        equipment = Networkequipment.objects.get(ip=ip)
        user = NetconfUsers.objects.filter(equipment=equipment)[0]
        unniType = UnitType.objects.filter(networkequipment__ip=ip)[0]

        # 2. 查询支持的模板 和模板类型
        try:
            template = unniType.templates_set.all().filter(tempType__name='VLAN配置模板')[0]
            serializers = TemplatesSerializers(template)

            # 3. 获取到配置模板
            template_xml_string = serializers.data.get('templateData')

            # 5，获取配置参数列表
            params = template.params_set.all()
            # paramsList = []
            # for item in params:
            #     paramsSerializers = ParamsSerializers(item)
            #     paramsList.append(paramsSerializers.data)
        except Exception as e:
            print(e)
            return Response({'msg': '获取模板失败！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return user, template_xml_string, params

    def eidt_config(self, ip, user, data):
        """
        连接设备并下发配置
        :param ip: 设备IP（string）
        :param user: netconf用户（netconfuser moder object）
        :param data: 配置xml数据（string）
        :return: 返回设备返回xml并序列化会json数据（json）
        """
        try:
            # 5.使用设备用户连接设备
            connect = manager.connect(host=ip, port=user.port, username=user.username,
                                      password=user.password, hostkey_verify=False,
                                      device_params={'name': user.device_params},
                                      allow_agent=False, look_for_keys=False)

            with connect as m:
                reply_obj = m.edit_config(target='running', config=data)
                reply_json_data = xmltodict.parse(str(reply_obj))
            return reply_json_data
        except Exception as e:
            return e

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        创建vlan
        """
        # print(request.data)
        # {'ip': '192.168.100.200', 'vlan': {'vlanId': '11', 'vlanName': '111', 'vlanDesc': '111'}}
        ip = request.data.get('ip')
        # 1. 根据IP查询相关信息
        user, template_xml_string, params = self.getInfo(ip)
        # 2. 获取create-template元素的内容
        domTree = parseString(template_xml_string)
        template_create_xml = domTree.getElementsByTagName('tempalte-create')[0].childNodes[1].toxml()
        # 3. 构造报文
        config_temp = Template(template_create_xml)
        # 3.1 构造mapping
        vlan_data = request.data.get('vlan')
        mapping = {}
        for item in params:
            # name值作为key, 数据作为value
            mapping[item.name] = vlan_data.get(item.name)
        # 3.2 替换参数,生程string类型的xml报文数据
        config_data = config_temp.substitute(mapping)

        # 4. 下发配置
        reply = self.eidt_config(ip=ip, user=user, data=config_data)
        # BUG:如果处理配置错误的问题？ //The name has been used by another VLAN.
        print(reply)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     """删除vlan"""
    #     # 1. 获取到设备的信息
    #     # 2. 获取到设备的配置模板
    #     # 3. 构建mapping
    #     # 4. 构建报文
    #     # 5. 下发报文
    #     # 6. 返回结果
    #     pass

    def destroy(self, request, *args, **kwargs):
        """
        删除vlan
        """
        # request.data: {'ip': '192.168.100.200', 'vlan': {'vlanId': '11', 'vlanName': '111', 'vlanDesc': '111'}}
        ip = request.data.get('ip')
        # 1. 根据IP查询相关信息
        user, template_xml_string, params = self.getInfo(ip)
        # 2. 获取create-template元素的内容
        domTree = parseString(template_xml_string)
        """ 
        添加和删除不同仅在获取不同的模板
        getElementsByTagName('tempalte-delete')
        """
        template_create_xml = domTree.getElementsByTagName('tempalte-delete')[0].childNodes[1].toxml()
        # 3. 构造报文
        config_temp = Template(template_create_xml)
        # 3.1 构造mapping
        vlan_data = request.data.get('vlan')
        mapping = {}
        for item in params:
            # name值作为key, 数据作为value
            mapping[item.name] = vlan_data.get(item.name)
        # 3.2 替换参数,生程string类型的xml报文数据
        config_data = config_temp.substitute(mapping)

        # 4. 下发配置
        reply = self.eidt_config(ip=ip, user=user, data=config_data)
        # BUG:如果处理配置错误的问题？ //The name has been used by another VLAN.
        print(reply)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)

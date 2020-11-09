from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from CMS.apps.configManage.serializers import  ParamsSerializers
from ncclient import manager
from xml.dom.minidom import  parseString
import xmltodict
from string import Template
from CMS.apps.tools.configTools import edit_config, getInfo


class VlansViews(GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        获取vlan列表，并返回配置参数（）
        """

        ip = request.query_params.get('ip')
        try:
            # 1. 根据ip查到设备信息：netconf user信息, 模板信息
            user, template_xml_string, params = getInfo(ip=ip, tempTypeName='VLAN配置模板')

            # 2. 获取get-template元素的内容
            domTree = parseString(template_xml_string)
            template_get_xml = domTree.getElementsByTagName('tempalte-get')[0].childNodes[1].toxml()
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

    def create(self, request, *args, **kwargs):
        """
        创建vlan
        """
        # print(request.data)
        # {'ip': '192.168.100.200', 'vlan': {'vlanId': '11', 'vlanName': '111', 'vlanDesc': '111'}}
        ip = request.data.get('ip')
        # 1. 根据IP查询相关信息
        user, template_xml_string, params = getInfo(ip, tempTypeName='VLAN配置模板')
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
        try:
        # 4. 下发配置
            reply = edit_config(ip=ip, user=user, data=config_data)
            # error:如果处理配置错误的问题？ //The name has been used by another VLAN.
        except Exception as e:
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        删除vlan
        """
        # kwargs.pk = vlanId
        # request.data: {'ip': '192.168.100.200', 'vlan': {'vlanId': '11', 'vlanName': '111', 'vlanDesc': '111'}}
        ip = request.data.get('ip')
        # 1. 根据IP查询相关信息
        user, template_xml_string, params = getInfo(ip, tempTypeName='VLAN配置模板')
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
        try:
            # 4. 下发配置
            reply = edit_config(ip=ip, user=user, data=config_data)
            # BUG:如果处理配置错误的问题？ //The name has been used by another VLAN.
            print(reply)
        except Exception as e:
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)

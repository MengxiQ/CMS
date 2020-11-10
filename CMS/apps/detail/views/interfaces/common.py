from string import Template
from xml.dom.minidom import parseString

from rest_framework import status
from rest_framework.response import Response

from CMS.apps.tools.configTools import edit_config, getInfo
from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class CommonInterfacesViews(ConfigAPIVies):
    functionName = '配置设备接口基本信息'
    def create(self, request, *args, **kwargs):
        """
        创建配置
        request.data
        {
        ip: this.ip,
        data: this.temp
        }
        """

        # print(request.data)
        # {'ip': '192.168.100.200', 'vlan': {'vlanId': '11', 'vlanName': '111', 'vlanDesc': '111'}}
        ip = request.data.get('ip')
        # 1. 根据IP查询相关信息
        user, template_xml_string, params = getInfo(ip, functionName=self.functionName)
        # 2. 获取create-template元素的内容
        domTree = parseString(template_xml_string)
        # template_create_xml = domTree.getElementsByTagName(self.create_TagName)[0].childNodes[1].toxml()

        # 3. 构造报文

        # 3.1 构造mapping
        request_data = request.data.get('data')
        mapping = {}
        NoneParams = []  # 空的标签名
        for item in params:
            # name值作为key, 数据作为value
            # print(request_data.get(item.name))
            if request_data.get(item.name) is None:
                NoneParams.append(item.name)
            mapping[item.name] = request_data.get(item.name)

        # 删除掉空的标签
        template_create_dom = domTree.getElementsByTagName(self.create_TagName)[0].childNodes[1]
        # for item in NoneParams:
        #     dom = domTree.getElementsByTagName(item)[0]
        #     dom.parentNode.removeChild(dom)

        # 如果接口为二层接口(或者IP地址为空)，则删除三层接口的标签

        print(request_data.get('ifIpAddr'))
        if (request_data.get('isL2SwitchPort') == 'true' or request_data.get('ifIpAddr') == None):
            dom = template_create_dom.getElementsByTagName('ifmAm4')[0]
            dom.parentNode.removeChild(dom)
        template_create_xml =template_create_dom.toxml()
        # 3.2 替换参数,生程string类型的xml报文数据
        config_temp = Template(template_create_xml)
        config_data = config_temp.substitute(mapping)
        print(config_data)
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
        删除配置
        """
        # kwargs.pk = vlanId
        # request.data: {'ip': '192.168.100.200', 'vlan': {'vlanId': '11', 'vlanName': '111', 'vlanDesc': '111'}}
        ip = request.data.get('ip')
        # 1. 根据IP查询相关信息
        user, template_xml_string, params = getInfo(ip, functionName=self.functionName)
        # 2. 获取create-template元素的内容
        domTree = parseString(template_xml_string)
        """ 
        添加和删除不同仅在获取不同的模板
        getElementsByTagName('tempalte-delete')
        """
        template_delete_dom = domTree.getElementsByTagName(self.delete_TagName)[0].childNodes[1]

        operation = request.data.get('operation')

        if operation == 'delete-interface' :
            # 删除接口，则删除ipv4标签
            dom = template_delete_dom.getElementsByTagName('ifmAm4')[0]
            dom.parentNode.removeChild(dom)
        else:
        # 如果是删除IP  interface operation="merge"
            dom = template_delete_dom.getElementsByTagName('interface')[0]
            dom.setAttribute('operation', 'merge')
        # 3. 构造报文
        config_temp = Template(template_delete_dom.toxml())
        # 3.1 构造mapping
        vlan_data = request.data.get('data')
        mapping = {}
        for item in params:
            # name值作为key, 数据作为value
            mapping[item.name] = vlan_data.get(item.name)
        # 3.2 替换参数,生程string类型的xml报文数据
        config_data = config_temp.substitute(mapping)
        print(config_data)
        try:
            # 4. 下发配置
            reply = edit_config(ip=ip, user=user, data=config_data)
            # BUG:如果处理配置错误的问题？ //The name has been used by another VLAN.
            # print(reply)
        except Exception as e:
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)
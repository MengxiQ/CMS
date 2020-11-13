from string import Template
from xml.dom.minidom import parseString

from rest_framework import status
from rest_framework.response import Response

from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies
from CMS.apps.tools.configTools import getInfo, edit_config


class VlansViews(ConfigAPIVies):
    functionName = '增删改查vlan信息'  # 必要，配置模板的功能名称

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
            print(reply)
        except Exception as e:
            print(e)
            # 如果vlanif接口被删除，那么就会出现下问题
            if str(e) == 'The VLANIF does not exist.':
                # 把vlanif标签去掉
                dom = template_delete_dom.getElementsByTagName('vlanif')[0]
                dom.parentNode.removeChild(dom)
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
                    print(reply)
                except Exception as e:
                    return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)

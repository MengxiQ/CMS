from string import Template
from xml.dom.minidom import parseString

from rest_framework import status
from rest_framework.response import Response

from CMS.apps.tools.configTools import edit_config, getInfo
from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies
import re

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

        template_create_dom = domTree.getElementsByTagName(self.create_TagName)[0].childNodes[1]

        # 删除掉空的标签
        NoneParams = []  # 空的标签名
        mapping = {}
        for item in params:
            if request_data.get(item.name) is None:
                NoneParams.append(item.name)
            mapping[item.name] = request_data.get(item.name)

        for item in NoneParams:
            dom = template_create_dom.getElementsByTagName(item)[0]
            dom.parentNode.removeChild(dom)

        # 如果接口为二层接口(或者IP地址为空)，则删除三层接口的标签
        print('l2Enable', request_data.get('l2Enable'))
        if request_data.get('l2Enable') == 'disable' or request_data.get('ifIpAddr') == '' or request_data.get('ifIpAddr') is None:
            dom = template_create_dom.getElementsByTagName('ifmAm4')[0]
            dom.parentNode.removeChild(dom)

        # 3.2 替换参数,生程string类型的xml报文数据
        config_temp = Template(template_create_dom.toxml())
        config_data = config_temp.substitute(mapping)
        print(config_data)
        try:
            # 4. 下发配置
            reply = edit_config(ip=ip, user=user, data=config_data)
        except Exception as e:
            print(e)
            # 配置vlanif接口，如果vlan配置下的vlanif接口被删除，引发以下错误
            # The ifName does not exist.
            if str(e) == 'The ifName does not exist.':
                # 1、执行更新vlan的配置，激活vlan配置下的vlanif接口
                config_temp = Template("""<config>
                    <vlan xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
                        <vlans>
                            <vlan>
                                <vlanId>${vlanId}</vlanId>
                                   <vlanif>
                                       <ifName>Vlanif${vlanId}</ifName>
                                       <cfgBand>1000</cfgBand>
                                       <dampTime>0</dampTime>
                                    </vlanif>
                            </vlan>
                        </vlans>
                    </vlan>
                </config>""")
                # ifName: "Vlanif200"
                ifName = request_data.get('ifName')
                # 提取出vlanId
                vlanId = re.match(r'Vlanif(\d+)', ifName).group(1)
                config_data = config_temp.substitute(vlanId=vlanId)
                print(config_data)
                try:
                    # 4. 下发配置
                    reply = edit_config(ip=ip, user=user, data=config_data)
                    # 重新添加接口
                    self.create(request, *args, **kwargs)
                except:
                    return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Please delete the commands that are not supported after the switching. //必须删除二层接口相关的配置才能配置成三层接口。
            if str(e) == 'Please delete the commands that are not supported after the switching.':
                return Response({'msg': '必须删除二层接口相关的配置才能配置成三层接口！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
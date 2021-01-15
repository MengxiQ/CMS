from string import Template
from xml.dom.minidom import parseString
from rest_framework import status
from rest_framework.response import Response

from CMS.apps.typesManage.serializers.TypeSerializers import ParamsSerializers
from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies
from CMS.apps.tools.vlansTools import Vlans2List, List2Vlans, List2Vlanserge


class EthernetInterfacesViews(ConfigAPIVies):
    functionName = '配置以太接口'

    def list(self, request, *args, **kwargs):
        """
        获取返回配置列表，并返回配置参数列表
        """
        # 配置数据源
        source = request.data.get('source')
        if source is not None:
            self.source = source
        ip = request.query_params.get('ip')
        # 1. 根据ip查到设备信息：netconf user信息, 模板信息
        user, template_xml_string, params = self.getInfo(ip=ip, functionName=self.functionName)
        # 2. 获取get-template元素的内容
        try:
            domTree = parseString(template_xml_string)
            template_get_xml = domTree.getElementsByTagName(self.get_TagName)[0].childNodes[1].toxml()
        except Exception as e:
            print(e)
            return Response({'msg': 'XML模板语法错误。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        paramsList = []
        for item in params:
            paramsSerializers = ParamsSerializers(item)
            paramsList.append(paramsSerializers.data)
        try:
            res = self.get_config(ip, user, template_get_xml)
            interfances = res['ethernet']['ethernetIfs']['ethernetIf']
            for interfance in interfances:
                if interfance['l2Enable'] == 'enable':
                    trunkVlans = interfance['l2Attribute']['trunkVlans']
                    if trunkVlans is not None:
                        interfance['l2Attribute']['trunkVlans'] = (Vlans2List(interfance['l2Attribute']['trunkVlans']))
        except Exception as e:
            print(e)
            return Response({'msg': '配置模板错误：' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'data': res, 'params': paramsList}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        创建配置
        request.data
        {
        ip: this.ip,
        data: this.temp
        }
        """
        # 配置数据源
        source = request.data.get('source')
        if source is not None:
            self.source = source
        # print(request.data)
        # {'ip': '192.168.100.200', 'vlan': {'vlanId': '11', 'vlanName': '111', 'vlanDesc': '111'}}
        ip = request.data.get('ip')
        # 1. 根据IP查询相关信息
        user, template_xml_string, params = self.getInfo(ip, functionName=self.functionName)
        # 2. 获取create-template元素的内容
        domTree = parseString(template_xml_string)
        # template_create_xml = domTree.getElementsByTagName(self.create_TagName)[0].childNodes[1].toxml()
        data = request.data.get('data')
        # 3. 构造报文
        # 删除掉空的标签
        template_create_dom = domTree.getElementsByTagName(self.create_TagName)[0].childNodes[1]
        if (data.get('linkType') == '"access"' or data.get('trunkVlans') == None):
            dom = template_create_dom.getElementsByTagName('trunkVlans')[0]
            dom.parentNode.removeChild(dom)
        else:
            # 如果是trunk接口，而且trunkVlans不为Node,根据vlans列表生成vlans字符串赋值给trunkVlans
            vlans = List2Vlans(vlans_list=data['trunkVlans'])
            update_vlans = List2Vlanserge(data.get('oldTrunkVlans'), data['trunkVlans'])
            data['trunkVlans'] = vlans + ':' + update_vlans
        # 3.1 构造mapping
        mapping = {}
        NoneParams = []  # 空的标签名
        for item in params:
            # name值作为key, 数据作为value
            # print(data.get(item.name))
            if data.get(item.name) is None:
                NoneParams.append(item.name)
            mapping[item.name] = data.get(item.name)

        # for item in NoneParams:
        #     dom = domTree.getElementsByTagName(item)[0]
        #     dom.parentNode.removeChild(dom)
        template_create_xml =template_create_dom.toxml()

        # print(template_create_xml)
        # 3.2 替换参数,生程string类型的xml报文数据
        config_temp = Template(template_create_xml)
        config_data = config_temp.substitute(mapping)
        # print(config_data)
        try:
            # 4. 下发配置
            reply = self.edit_config(ip=ip, user=user, config=config_data)
            # error:如果处理配置错误的问题？ //The name has been used by another VLAN.
        except Exception as e:
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)


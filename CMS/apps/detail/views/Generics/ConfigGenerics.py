from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from CMS.apps.configManage.serializers import ParamsSerializers
from ncclient import manager
from xml.dom.minidom import parseString
import xmltodict
from string import Template
from CMS.apps.tools.configTools import edit_config, getInfo


class ConfigAPIVies(GenericAPIView):
    # 重写类属性或者方法，自定义
    functionName = ''  # 必要，配置模板的功能名称
    get_TagName = 'tempalte-get'  # xml配置模板里获取配置信息的根标签
    delete_TagName = 'tempalte-delete'  # xml配置模板里删除配置的根标签
    create_TagName = 'tempalte-create'  # xml配置模板里创建配置的根标签

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        获取返回配置列表，并返回配置参数列表
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
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': reply_json_data['rpc-reply']['data'], 'params': paramsList},
                        status=status.HTTP_200_OK)

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
        for item in NoneParams:
            dom = template_create_dom.getElementsByTagName(item)[0]
            dom.parentNode.removeChild(dom)
        # dom = domTree.getElementsByTagName('addrType')[0]
        # dom.parentNode.removeChild(dom)
        template_create_xml = template_create_dom.toxml()
        # print(template_create_xml)
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
        global dom
        ip = request.data.get('ip')
        # 1. 根据IP查询相关信息
        user, template_xml_string, params = getInfo(ip, functionName=self.functionName)
        # 2. 获取create-template元素的内容
        domTree = parseString(template_xml_string)

        template_delete_dom = domTree.getElementsByTagName(self.delete_TagName)[0].childNodes[1]

        request_data = request.data.get('data')

        # 删除掉空的标签
        NoneParams = []  # 空的标签名
        mapping = {}
        for item in params:
            # name值作为key, 数据作为value
            # print(request_data.get(item.name))
            if request_data.get(item.name) is None:
                NoneParams.append(item.name)
            mapping[item.name] = request_data.get(item.name)

        for item in NoneParams:
            doms = template_delete_dom.getElementsByTagName(item)
            # 防止模板中没有空元素的标签，而返回错误
            if doms:
                dom = doms[0]
                dom.parentNode.removeChild(dom)
            else:
                pass
        config_temp = Template(template_delete_dom.toxml())

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
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)

    def params(self, request, *args, **kwargs):
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

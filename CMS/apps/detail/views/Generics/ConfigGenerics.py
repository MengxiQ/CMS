from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.utils import json

from CMS.apps.typesManage.serializers.TypeSerializers import ParamsSerializers
from xml.dom.minidom import parseString
from string import Template
from CMS.apps.detail.views.Generics.GetUserInfo import GetUserInfo
from CMS.apps.detail.views.Generics.configTools import ConfigTools


class ConfigAPIVies(GenericAPIView, ConfigTools, GetUserInfo):
    # 重写类属性或者方法，自定义
    functionName = ''  # 必要，配置模板的功能名称
    get_TagName = 'tempalte-get'  # xml配置模板里获取配置信息的根标签
    delete_TagName = 'tempalte-delete'  # xml配置模板里删除配置的根标签
    create_TagName = 'tempalte-merge'  # xml配置模板里创建配置的根标签

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def list(self, request, getConfig=True, *args, **kwargs):
        """
        获取返回配置列表，并返回配置参数列表,
        getConfig : False,则执行 m.get()
        """
        # 配置数据源
        source = request.query_params.get('source')
        if source is not None:
            self.source = source

        ip = request.query_params.get('ip')
        # 1. 根据ip查到设备信息：netconf user信息, 模板信息
        try:
            user, template_xml_string, params, position = self.getInfo(ip=ip, functionName=self.functionName)
            if position is None:
                return Response({'msg': '模板没有配置position.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 2. 整个模板XML生成domTree
        try:
            domTree = parseString(template_xml_string)
        except Exception as e:
            return Response({'msg': '模板错误-' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 3. 构造报文
        # 获取get的标签内容
        template_get_dom = domTree.getElementsByTagName(self.get_TagName)[0].childNodes[1]

        # 参数列表
        paramsList = []
        for item in params:
            paramsSerializers = ParamsSerializers(item)
            paramsList.append(paramsSerializers.data)

        # 3.1 构造mapping
        # print(request.query_params)
        request_data = request.query_params.get('data')
        # print(request_data)
        config_data = {}
        if request_data is None:
            # 如果data为空，则直接将模板内容下发
            config_data = template_get_dom.toxml()
        else:
            # 替换模板参数
            # query参数的内层对象为为字符串，转json
            request_data = json.loads(request_data)
            print(request_data)
            mapping = {}
            # NoneParams = []  # 空的标签名
            for item in params:
                # name值作为key, 数据作为value
                # print(request_data.get(item.name))
                # if request_data.get(item.name) is None:
                #     NoneParams.append(item.name)
                mapping[item.name] = request_data.get(item.name)

            # # 删除掉空的标签
            # print(NoneParams)
            # if NoneParams is not None:
            #     for item in NoneParams:
            #         dom = template_get_dom.getElementsByTagName(item)[0]
            #         dom.parentNode.removeChild(dom)
            template_get_xml = template_get_dom.toxml()
            # 3.2 替换参数,生程string类型的xml报文数据
            config_temp = Template(template_get_xml)
            config_data = config_temp.substitute(mapping)
            # print(config_data)
        try:
            if getConfig:
                res = self.get_config(ip, user, config_data, position)
            else:
                res = self.get_info(ip, user, config_data)
        except Exception as e:
            # 下发配置错误需要重新连接设备，保存会话
            # self.restConnect(ip, user)
            print(e)
            return Response({'msg': str(e), 'params': paramsList}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'data': res, 'params': paramsList}, status=status.HTTP_200_OK)

    def create(self, request, isAction=False, *args, **kwargs):
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
        # //
        # print(request.data)
        ip = request.data.get('ip')
        # 1. 根据IP查询相关信息
        user, template_xml_string, params, position = self.getInfo(ip, functionName=self.functionName)
        # 2. 获取create-template元素的内容
        domTree = parseString(template_xml_string)
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
        template_create_xml = template_create_dom.toxml()
        # print(template_create_xml)
        # 3.2 替换参数,生程string类型的xml报文数据
        config_temp = Template(template_create_xml)
        config_data = config_temp.substitute(mapping)
        # print(config_data)
        try:
            print('isAction:', isAction)
            if not isAction:
                self.edit_config(ip, user, config_data)
            else:
                self.action(ip, user, config_data)
        except Exception as e:
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)

    def destroy(self, request, isAction=True, *args, **kwargs):
        """
        删除配置
        """
        source = request.data.get('source')
        if source is not None:
            self.source = source
        ip = request.data.get('ip')
        # 1. 根据IP查询相关信息
        user, template_xml_string, params, position = self.getInfo(ip, functionName=self.functionName)
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
        try:
            if isAction:
                reply = self.edit_config(ip=ip, user=user, config=config_data)
            else:
                reply = self.action(ip=ip, user=user, config=config_data)
        except Exception as e:
            print(e)
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'ok'}, status=status.HTTP_200_OK)

    def params(self, request, *args, **kwargs):
        """
        返回配置参数列表
        """
        ip = request.query_params.get('ip')
        try:
            user, template_xml_string, params = self.getInfo(ip=ip, functionName=self.functionName)
            paramsList = []
            for item in params:
                paramsSerializers = ParamsSerializers(item)
                paramsList.append(paramsSerializers.data)

        except Exception as e:
            print(e)
            return Response({'msg': '获取模板失败！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': '', 'params': paramsList}, status=status.HTTP_200_OK)

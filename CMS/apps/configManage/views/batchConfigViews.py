from string import Template
from xml.dom.minidom import parseString

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class GenerateConfig(GenericAPIView):
    get_TagName = 'tempalte-get'  # xml配置模板里获取配置信息的根标签
    delete_TagName = 'tempalte-delete'  # xml配置模板里删除配置的根标签
    create_TagName = 'tempalte-create'  # xml配置模板里创建配置的根标签
    def post(self, request):
        print(request.data)
        domTree = parseString(request.data.get('template'))
        # 3. 构造报文
        # 3.1 构造mapping
        mapping = request.data.get('temp')
        template_create_dom = domTree.getElementsByTagName(self.create_TagName)[0].childNodes[1]
        template_create_xml = template_create_dom.toxml()
        # print(template_create_xml)
        # 3.2 替换参数,生程string类型的xml报文数据
        config_temp = Template(template_create_xml)
        config_data = config_temp.substitute(mapping)
        return Response({'data': config_data}, status=status.HTTP_200_OK)
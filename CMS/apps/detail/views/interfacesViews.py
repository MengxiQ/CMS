import json

import xmltodict
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,CreateModelMixin,DestroyModelMixin,UpdateModelMixin,RetrieveModelMixin
from CMS.apps.equipment.models import Networkequipment
from CMS.controller.configuration.search import Search
from ..models import Interfaces
from ..serializers import InterfacesSerializers


class GatherInterfaces(GenericAPIView):
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesSerializers

    def gather(self, request):
        # 获取设备型号,设备ip
        ip = request.query_params.get('ip')

        equipment = Networkequipment.objects.get(ip=ip)
        # netype?
        # 查询设备接口采集模板
        # 连接设备
        search = Search()
        # 采集接口数据
        interface_getall = '''
        <filter type="subtree">
          <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
            <interfaces>
              <interface>
              
              </interface>
            </interfaces>
          </ifm>
        </filter>
        '''
        XMLdata = search.get(interface_getall)
        convertJson = xmltodict.parse(str(XMLdata))
        interfaces = convertJson['rpc-reply']['data']['ifm']['interfaces']['interface']

        # 查询到所有的接口对象
        interfaces_objs = self.queryset.filter(equipment__ip=ip)

        for interface in interfaces:
            # 获取接口名称
            ifName = str(interface['ifName'])

            ipv4Config = json.dumps(interface['ipv4Config'])
            ipv6Config = json.dumps(interface['ipv6Config'])

            del interface['ipv4Config']
            del interface['ipv6Config']
            del interface['ifmAm4']
            del interface['ifmAm6']
            baseConfig = json.dumps(interface)

            # 判断对象是否存在
            print()
            if (len(interfaces_objs) != 0):
                interfaces_obj = interfaces_objs.get(ifName=ifName)
            else:
                interfaces_obj = False
            # print('interfaces_obj', interfaces_obj)
            if not(interfaces_obj):
                print('创建接口信息')
                # 创建接口信息
                new_interface = Interfaces.objects.create(ifName=ifName,
                                                            ipv4Config=ipv4Config,
                                                            ipv6Config=ipv6Config,
                                                            baseConfig=baseConfig,
                                                            equipment=equipment)
            else:
                print('更新接口信息')
                interface.update(ifName=ifName,
                                          ipv4Config=ipv4Config,
                                          ipv6Config=ipv6Config,
                                          baseConfig=baseConfig,
                                          equipment=equipment)




        rep_data = Interfaces.objects.filter(equipment__ip = ip)
        serializer = self.serializer_class(rep_data,many=True)
        return Response(serializer.data)

    def get(self, request):
        return self.gather(request)


class InterfacesViews(GenericAPIView, ListModelMixin,
                      CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):

    queryset = Interfaces.objects.all()
    serializer_class = InterfacesSerializers
    # lookup_field = ('ip')

    def get(self, request):
        ip = request.query_params['ip']
        interfaces = self.queryset.filter(equipment__ip=ip)
        serializer = self.serializer_class(interfaces, many=True)
        return Response(serializer.data)




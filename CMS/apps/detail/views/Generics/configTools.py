import xmltodict
from ncclient import manager
from rest_framework import status
from rest_framework.response import Response

from CMS.apps.configManage.serializers import TemplatesSerializers
from CMS.apps.equipment.models import Networkequipment, NetconfUsers, UnitType
from django.conf import settings


class ConfigTools:
    def getInfo(self, ip, functionName):
        """
        获取设备相关信息
        :param tempTypeName:
        :param self: 设备的IP地址, tempTypeName:模板名称
        :return: 返回的是一个字典
        {
        user：netconf账户（model object）
        template_xml_string：string形式的配置模板信息（string）
        params: 参数列表（Questet List）
        }
        """
        """
        连接设备，必须要等上一个任务完成了，才能执行下一个连接。
        所以需要以队列的方式处理
        """
        try:
            equipment = Networkequipment.objects.get(ip=ip)
            user = equipment.user
            unniType = UnitType.objects.filter(networkequipment__ip=ip)[0]

            # 2. 查询支持的模板 和模板类型
            template = unniType.templates_set.all().filter(function__name=functionName)[0]
            serializers = TemplatesSerializers(template)

            # 3. 获取到配置模板
            template_xml_string = serializers.data.get('templateData')

            # 5，获取配置参数列表
            params = template.params_set.all()
        except Exception as e:
            print(e)
            return Response({'msg': '获取模板失败！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return user, template_xml_string, params

    def connect(self, ip,  user):
        # 返回连接对象
        try:
            # 5.使用设备用户连接设备
            # 先判断是否打开连接
            sessions = settings.SSH_SESSION
            flag = -1
            for index, item in enumerate(sessions):
                if sessions[index]['ip'] == ip:
                    m = sessions[index]['connect']
                    flag = index
            if flag == -1:
                connect = manager.connect(host=ip, port=user.port, username=user.username,
                                              password=user.password, hostkey_verify=False,
                                              device_params={'name': user.device_params},
                                              allow_agent=False, look_for_keys=False)
                settings.SSH_SESSION.append({'ip': ip, 'connect': connect})
                m = connect
            return m
        except Exception as e:
            print(e)
            return Response({'msg': '连接设备错误：' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def restConnect(self, ip, user):
        # 重置连接
        try:
            session = {}
            sessions = settings.SSH_SESSION
            for index, item in enumerate(sessions):
                if sessions[index]['ip'] == ip:
                    session = sessions[index]
            session['connect'] = manager.connect(host=ip, port=user.port, username=user.username,
                                              password=user.password, hostkey_verify=False,
                                              device_params={'name': user.device_params},
                                              allow_agent=False, look_for_keys=False)
        except Exception as e:
            print(e)
            return Response({'msg': '连接设备错误：' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_config(self, ip, user, filter):
        m = self.connect(ip, user)
        # 返回data标签里的数据
        try:
            reply_obj = m.get_config(source='running', filter=filter)
            reply_json_data = xmltodict.parse(str(reply_obj))
            return reply_json_data['rpc-reply']['data']
        except Exception as e:
            # 下发配置错误需要重新连接设备，保存会话
            self.restConnect(ip, user)
            print(e)
            return Response({'msg': '配置模板错误：' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def edit_config(self, ip, user, config):
        """
            连接设备并下发配置
            :param ip: 设备IP（string）
            :param user: netconf用户（netconfuser moder object）
            :param config: 配置xml数据（string）
            :return: 返回设备返回xml并序列化会json数据（json）
            """
        m = self.connect(ip, user)
        try:
            reply_obj = m.edit_config(target='running', config=config)
            reply_json_data = xmltodict.parse(str(reply_obj))
        except Exception as e:
            # 下发配置错误需要重新连接设备，保存会话
            self.restConnect(ip, user)
            print(e)
            return Response({'msg': '配置错误：' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return reply_json_data

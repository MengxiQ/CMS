import xmltodict
from ncclient import manager
from rest_framework import status
from rest_framework.response import Response

from CMS.apps.configManage.serializers import TemplatesSerializers
from CMS.apps.equipment.models import Networkequipment, NetconfUsers, UnitType

"""调用下面的函数请捕获异常"""


def getInfo(ip, functionName):
    """
    获取设备相关信息
    :param tempTypeName:
    :param ip: 设备的IP地址, tempTypeName:模板名称
    :return: 返回的是一个字典
    {
    user：netconf账户（model object）
    template_xml_string：string形式的配置模板信息（string）
    params: 参数列表（Questet List）
    }
    """
    equipment = Networkequipment.objects.get(ip=ip)
    user = NetconfUsers.objects.filter(equipment=equipment)[0]
    unniType = UnitType.objects.filter(networkequipment__ip=ip)[0]

    # 2. 查询支持的模板 和模板类型
    template = unniType.templates_set.all().filter(function__name=functionName)[0]
    serializers = TemplatesSerializers(template)

    # 3. 获取到配置模板
    template_xml_string = serializers.data.get('templateData')

    # 5，获取配置参数列表
    params = template.params_set.all()

    return user, template_xml_string, params


def edit_config(ip, user, data):
    """
        连接设备并下发配置
        :param ip: 设备IP（string）
        :param user: netconf用户（netconfuser moder object）
        :param data: 配置xml数据（string）
        :return: 返回设备返回xml并序列化会json数据（json）
        """
    # 5.使用设备用户连接设备
    connect = manager.connect(host=ip, port=user.port, username=user.username,
                              password=user.password, hostkey_verify=False,
                              device_params={'name': user.device_params},
                              allow_agent=False, look_for_keys=False)

    with connect as m:
        reply_obj = m.edit_config(target='running', config=data)
        reply_json_data = xmltodict.parse(str(reply_obj))
    return reply_json_data

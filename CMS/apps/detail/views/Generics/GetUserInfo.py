from CMS.apps.typesManage.serializers.TypeSerializers import TemplatesSerializers
from CMS.apps.equipment.models import Networkequipment, UnitType


class GetUserInfo:
    def getInfo(self, ip, functionName=None):
        """
        获取设备相关信息
        :param ip:
        :param functionName:
        :param tempTypeName: # 如果只需要用于信息设置为默认None
        :param self: 设备的IP地址, tempTypeName:模板名称
        :return: 返回的是一个字典
        {
        user：netconf账户（model object）
        template_xml_string：string形式的配置模板信息（string）
        params: 参数列表（Questet List）
        }
        """
        try:
            equipment = Networkequipment.objects.get(ip=ip)
            user = equipment.user
            unniType = UnitType.objects.filter(networkequipment__ip=ip)[0]

            # 2. 查询支持的模板 和模板类型
            if functionName is not None:
                template = unniType.templates_set.all().filter(function__name=functionName)[0]
                serializers = TemplatesSerializers(template)
                # 3. 获取到配置模板
                template_xml_string = serializers.data.get('templateData')
                # 5，获取配置参数列表
                params = template.params_set.all()
            else:
                # 因为只想获取用户信息返回None
                template_xml_string = None
                params = None
        except Exception as e:
            print(e)
            raise Exception({'msg': '获取模板失败！'})

        return user, template_xml_string, params

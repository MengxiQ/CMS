import xmltodict
from ncclient.xml_ import new_ele, sub_ele, HW_PRIVATE_NS, validated_element

from CMS.apps.detail.views.Generics.Connector import Connector


class ConfigTools(Connector):
    """
    该类实现对NETCONF配置操作的实现
    """
    source = 'running'  # source属性用于指设备的配置库

    def get_info(self, ip, user, filter):
        """
        get_info方法实现对设备进行<get>操作.
        返回data标签里的数据.
        如果设备对应答报文进行了分包处理，则返回setId
        """
        m = self.connect(ip, user)
        reply_obj = m.get(filter=filter)
        reply_json_data = xmltodict.parse(str(reply_obj))
        setId =reply_json_data['rpc-reply'].get('@set-id')  # 如果不需要分包，则返回None，@set-id: None
        if setId is None:
            return reply_json_data['rpc-reply']['data']  # 返回装换的json数据
        else:
            # 需要分包处理，返回数据携带到setId
            data = reply_json_data['rpc-reply']['data']
            data['setId'] = setId
            return data

    def get_config(self, ip, user, filter):
        # 返回data标签里的数据
        m = self.connect(ip, user)
        reply_obj = m.get_config(source=self.source, filter=filter)
        reply_json_data = xmltodict.parse(str(reply_obj))
        return reply_json_data['rpc-reply']['data']  # 返回装换的json数据

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
            # print('self.source:', self.source)
            reply_obj = m.edit_config(target=self.source, config=config)
        except Exception as e:
            raise Exception(e)
        return xmltodict.parse(str(reply_obj))  # 返回装换的json数据

    def action(self, ip, user, config):
        # 增删action都是同一个方法
        m = self.connect(ip, user)
        try:
            xsd_fetch = new_ele("execute-action", attrs={"xmlns": HW_PRIVATE_NS})
            xsd_fetch.append(validated_element(config))
            reply_obj = m.dispatch(xsd_fetch)
        except Exception as e:
            raise Exception(e)
        return xmltodict.parse(str(reply_obj))  # 返回装换的json数据

    def get_next(self, ip, user, setId=None):
        # 获取下一个分包
        m = self.connect(ip, user)
        try:
            xsd_fetch = new_ele("get-next", attrs={"xmlns": HW_PRIVATE_NS, "set-id": setId})
            reply_obj = m.dispatch(xsd_fetch)
        except Exception as e:
            raise Exception(e)
        return xmltodict.parse(str(reply_obj))  # 返回装换的json数据




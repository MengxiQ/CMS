from CMS.controller.connections.connect import NetConfig
from CMS.controller.serializers.jsoner import Jsoner


class Search(NetConfig, Jsoner):
    ipaddr = '192.168.100.200'
    port = 22
    username = 'client001'
    password = 'Admin@wlx@2017'
    device_params = 'huawei'
    hostkey_verify = False
    connected = None
    # def __int__(self, ipaddr, port, username, device_params, hostkey_verify):
    #     self.ipaddr = ipaddr
    #     self.port = port
    #     self.username = username
    #     self.device_params = device_params
    #     self.hostkey_verify = hostkey_verify

    def __init__(self):
        self.connected = self.connect(ipaddr=self.ipaddr, port=self.port,
                               username=self.username, password=self.password,
                               device_params=self.device_params, hostkey_verify=self.hostkey_verify)
    def getAll(self):
        with self.connected as equipment:
            response = equipment.get()
        return response

    def get(self, xmldata):
        with self.connected as equipment:
            # return equipment.get_config(source='running', filter=('subtree',xmldata))
            return equipment.get_config(source='running', filter=xmldata)

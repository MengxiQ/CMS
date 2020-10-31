# import logging
from ncclient import manager
def set_int_vlan(ipaddr,int,vlan):
    # log=logging.getLogger(__name__)
    config ="""
    <config>
          <ethernet xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
            <ethernetIfs>
              <ethernetIf operation="merge">
                <ifName>"""+int+"""</ifName>
                <l2Attribute>
                  <linkType>access</linkType>
                  <pvid>"""+vlan+"""</pvid>
                </l2Attribute>
              </ethernetIf>
            </ethernetIfs>
          </ethernet>
    </config>
    """
    # print(config)
    huawei_connect = manager.connect(host=ipaddr,port=22,username='client001',
                               password='Admin@wlx@2017',hostkey_verify= False,
                               device_params={'name': "huawei"},
                               allow_agent = False,look_for_keys = False)
    rpc_obj = None
    with huawei_connect as m:
        rpc_obj = m.edit_config(target='running', config=config)
    return rpc_obj

print(set_int_vlan("192.168.100.200","GE1/0/2","20"))
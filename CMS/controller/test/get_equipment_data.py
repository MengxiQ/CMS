# log=logging.getLogger(__name__)
from ncclient import manager
config = """
<config>

</config>
"""
# print(config)
huawei_connect = manager.connect(host='192.168.100.200', port=22, username='client001',
                                 password='Admin@wlx@2017', hostkey_verify=False,
                                 device_params={'name': "huawei"},
                                 allow_agent=False, look_for_keys=False)
rpc_obj = None
with huawei_connect as m:
    rpc_obj = m.get()

print(rpc_obj)
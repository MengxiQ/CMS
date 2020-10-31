from ncclient import manager


# 只要是继承了这个类，那么就会有以下方法


class NetConfig:
    # 配置管理库
    manager = manager

    def connect(self, ipaddr, port, username, password, device_params='huawei', hostkey_verify=False):
        return self.manager.connect(host=ipaddr, port=port, username=username,
                                    password=password, hostkey_verify=hostkey_verify,
                                    device_params={'name': device_params},
                                    allow_agent=False, look_for_keys=False)

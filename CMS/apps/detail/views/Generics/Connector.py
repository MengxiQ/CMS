from django.conf import settings
from ncclient import manager


class Connector:
    """
    该类实现对纳管设备的NETCONF会话进行管理.
    connect方发实现会话的建立和保存，返回连接对象.
    disconnect方法用于关闭已打开的会话.
    """
    def connect(self, ip, user):
        # 返回连接对象
        m = {}
        try:
            # 5.使用设备用户连接设备
            # 先判断是否存在会话
            # 获取所有的连接对象
            sessions = settings.SSH_SESSION
            isExist = False  # 记录是否存在连接
            for index, item in enumerate(sessions):
                if sessions[index]['ip'] == ip:
                    # 存在连接
                    isExist = True
                    m = sessions[index]['connect']
                    print(ip + '-session-status:', m._session.connected)
                    # 判断会话连接是否打开
                    if not m._session.connected:  # m._session.connected: 连接打开，则返回true
                        # 连接存在，但没有打开，重新建立连接
                        m = sessions[index]['connect'] = manager.connect(host=ip, port=user.port,
                                                                         username=user.username,
                                                                         password=user.password, hostkey_verify=False,
                                                                         device_params={'name': user.device_params},
                                                                         allow_agent=False, look_for_keys=False)
            # 没有创建连接，创建连接
            if not isExist:
                m = connect = manager.connect(host=ip, port=user.port, username=user.username,
                                              password=user.password, hostkey_verify=False,
                                              device_params={'name': user.device_params},
                                              allow_agent=False, look_for_keys=False)
                settings.SSH_SESSION.append({'ip': ip, 'connect': connect})
            return m
        except Exception as e:
            print(e)
            raise Exception({'msg': '连接设备错误：' + str(e)})

    def disconnect(self, ip):
        # 关闭指定ip的连接， 返回布尔值
        m = {}
        try:
            # 5.使用设备用户连接设备
            # 先判断是否存在会话
            # 获取所有的连接对象
            sessions = settings.SSH_SESSION
            for index, item in enumerate(sessions):
                if sessions[index]['ip'] == ip:
                    # 存在连接
                    m = sessions[index]['connect']
                    print(ip + '-session-status:', m._session.connected)
                    # 判断会话连接是否打开
                    if m._session.connected:
                        # 连接打开，则关闭连接
                        try:
                            m.close_session()
                            return True
                        except Exception as e:
                            print(e)
                            return False
                    else:
                        # 连接没有打开，不需要操作
                        return True
        except Exception as e:
            print(e)
            return False

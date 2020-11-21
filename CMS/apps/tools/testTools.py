from datetime import datetime
from threading import Timer

# 定时尝试ping设备
from ping3 import ping

from CMS.apps.equipment.models import Networkequipment, NestatusType, Nestatus


def pingTimer(inc):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '刷新状态')
    # 1 查询所有的设备
    equipments = Networkequipment.objects.all()
    # 2 循环尝试ping设备
    for item in equipments:
        if ping_host(item.ip):
            # 更新状态类型
            data = {
                'date': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                'id': item.status_id,
                'remark': "在线",
                'site': "",
                'type_id': 1
            }
        else:
            # 更新状态类型
            data = {
                'date': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                'id': item.status_id,
                'remark': "离线",
                'site': "",
                'type_id': 2
            }
        # 2.1 写入状态
        type = NestatusType.objects.get(id=data.get('type_id'))  # type_id
        try:
            stat = Nestatus.objects.get(id=data.get('id'))
            stat.date = data.get('date')
            stat.remark = data.get('remark')
            stat.type = type
            stat.save()
        except Exception as e:
            print(e, '更新设备状态失败，尝试创建状态')
            # 1. 创建状态对象
            try:
                status_ins = Nestatus.objects.create(date=data.get('date'),
                                                     site=data.get('site'),
                                                     remark=data.get('remark'),
                                                     type_id=data.get('type_id')
                                                     )
                # 2. 关联
                item.status = status_ins
                item.save()
            except Exception as e:
                print(e, '尝试创建状态失败！')

    t = Timer(inc, pingTimer, (inc,))
    t.start()


def ping_host(ip_address):
    """
    获取节点的延迟的作用
    :param ip_address:
    :param node:
    :return: boolean
    """
    response = ping(ip_address)
    # print('ping:' + ip_address, response)
    if response is not None and response != False:
        return True
    else:
        return False
    # print(response)
    # if response is not None:
    #     delay = int(response * 1000)
    #     print(delay, "延迟")


def ping_text(ip, times):
    txt = []
    for item in range(times):
        res = ping(ip, timeout=2)
        if( res == False or res == None):
            text_out = 'ping \'' + ip + ' ... ' + 'time out.'
        else:
            text_out = 'ping \'' + ip + ' ... ' + str(round(res, 3) * 1000) + 'ms'
        print(text_out)
        txt.append(text_out)
    return txt

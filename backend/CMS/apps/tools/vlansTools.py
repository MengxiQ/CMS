import re


def Vlans2List(vlans_str, digits=1024):
    """传入vlans表达串，返回vlan清单列表"""
    # 华为规范，必须是1024位的十六进制字符串
    int10 = int(vlans_str, 16)
    bin2 = format(int10, '0' + str(digits * 4) + 'b')
    res = re.finditer('1', bin2)
    vlans = []
    for item in res:
        # item: <re.Match object; span=(300, 301), match='1'>
        vlans.append(item.span()[0])
    return vlans


def List2Vlans(vlans_list, digits=1024):
    """传入vlans清单列表，返回vlan表达串"""
    # 生成1024*4位二进制0字符串，转化成列表
    bin2_list = list(format(0, '0' + str(digits * 4) + 'b'))
    # 设置vlan号的位，置'1'
    for vlan in vlans_list:
        if isinstance(vlan, int):
            bin2_list[vlan] = '1'
        else:
            bin2_list[int(vlan)] = '1'
    # 再转化成字符串
    bin2_str = ''.join(bin2_list)
    # 将2进制字符串转化成十进制数
    int10 = int(bin2_str, 2)
    # 将十进制数转化成1204位16进制字符串表达式
    str16 = format(int10, '0' + str(digits) + 'X')
    return str16


def List2Vlanserge(vlans_list1, vlans_list2, digits=1024):
    """传入两个vlans清单列表，合并, 返回vlan表达串"""
    # 生成1024*4位二进制0字符串，转化成列表
    bin2_list = list(format(0, '0' + str(digits * 4) + 'b'))
    # 设置vlan号的位，置'1'
    if vlans_list1 is not None:
        for vlan1 in vlans_list1:
            try:
                if isinstance(vlan1, int):
                    bin2_list[vlan1] = '1'
                else:
                    if isinstance(vlan1, str):
                        bin2_list[int(vlan1)] = '1'
            except Exception as e:
                print(e)
                print('vlans中有非数字的标签，跳过。')

    if vlans_list2 is not None:
        for vlan2 in vlans_list2:
            try:
                if isinstance(vlan2, int):
                    bin2_list[vlan2] = '1'
                else:
                    if isinstance(vlan2, str):
                        bin2_list[int(vlan2)] = '1'
            except Exception as e:
                print(e)
                print('vlans中有非数字的标签，跳过。')
    # 再转化成字符串
    bin2_str = ''.join(bin2_list)
    # 将2进制字符串转化成十进制数
    int10 = int(bin2_str, 2)
    # 将十进制数转化成1204位16进制字符串表达式
    str16 = format(int10, '0' + str(digits) + 'X')
    return str16

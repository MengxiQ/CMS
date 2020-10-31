from xml.dom import minidom

dom = minidom.parse('getall_interfaces.xml')
interfaces = dom.getElementsByTagName('ethernetIf')
for interface in interfaces:
    ifname = interface.getElementsByTagName('ifName')[0].childNodes[0].data
    ifIndex = interface.getElementsByTagName('ifIndex')[0].childNodes[0].data
    l2Enable = interface.getElementsByTagName('l2Enable')[0].childNodes[0].data
    vlanAssigns = interface.getElementsByTagName('vlanAssigns')

    print(ifname, ifIndex, l2Enable)

import xmltodict
import json
with open('getall_interfaces.xml', 'r') as f:
    XMLdata = f.read()
# 这是一个字典
convertJson = xmltodict.parse(XMLdata)
ethernetIfs = convertJson['rpc-reply']['data']['ethernet']['ethernetIfs']['ethernetIf']
for ethernetIf in ethernetIfs:
    print(ethernetIf)

# JSONdata = json.dumps(convertJson)


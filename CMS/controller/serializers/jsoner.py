# 将模板xml配置模板序列化前端json
import json

import xmltodict


class Jsoner():
    def XMLtoJSON(self,XMLdata):
        convertJson = xmltodict.parse(str(XMLdata))
        return json.dumps(convertJson)
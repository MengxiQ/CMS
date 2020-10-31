# Press the green button in the gutter to run the script.
import xmltodict

from CMS.controller.configuration.search import Search

if __name__ == '__main__':
    search = Search()
    # XMLdata = search.getAll()
    interface_get = '''
        <filter type="subtree">
              <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
                <interfaces>
                  <interface>
                    <ifName>GE1/0/0</ifName>
                  </interface>
                </interfaces>
              </ifm>
            </filter>
    '''

    ## 注意
    # 1. 有值的标签表示过滤
    # 2. 空标签表示期待返回的字段值

    interface_getall = '''
    <filter type="subtree">
      <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <interfaces>
          <interface>
           
          </interface>
        </interfaces>
      </ifm>
    </filter>
    '''
    # XMLdata = search.get(interface_getall)
    XMLdata = search.getAll()
    print(search.XMLtoJSON(XMLdata))
    # print(XMLdata)
    # convertJson = xmltodict.parse(str(XMLdata))
    # ethernetIfs = convertJson['rpc-reply']['data']['ethernet']['ethernetIfs']['ethernetIf']
    # print(ethernetIfs)


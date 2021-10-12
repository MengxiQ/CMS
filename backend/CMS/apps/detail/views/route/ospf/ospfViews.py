from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class OspfProcessView(ConfigAPIVies):
    functionName = '配置ospfv2进程'


class OspfAreaView(ConfigAPIVies):
    functionName = '配置ospfv2区域'


class OspfAreaNetwork(ConfigAPIVies):
    functionName = '配置ospf区域网络'


class OspfAdvanceView(ConfigAPIVies):
    functionName = '配置ospf高级配置'


class OspfImportView(ConfigAPIVies):
    functionName = 'OSPF高级配置-路由发布'


class OspfDefaultAdviseView(ConfigAPIVies):
    functionName = '配置OSPF默认路由发布'
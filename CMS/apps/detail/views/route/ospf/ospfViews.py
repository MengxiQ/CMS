from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class OspfViews(ConfigAPIVies):
    functionName = '获取ospf信息'  # 必要，配置模板的名称


class OspfProcessView(ConfigAPIVies):
    functionName = '配置ospfv2进程'


class OspfAreaView(ConfigAPIVies):
    functionName = '配置ospfv2区域'

    def list(self, request, *args, **kwargs):
        return self.params(request, *args, **kwargs)


class OspfAreaNetwork(ConfigAPIVies):
    functionName = '配置ospf区域网络'

    def list(self, request, *args, **kwargs):
        return self.params(request, *args, **kwargs)


class OspfAdvanceView(ConfigAPIVies):
    functionName = '配置ospf高级配置'


class OspfDefaultAdviseView(ConfigAPIVies):
    functionName = '配置OSPF默认路由发布'

    def get(self, request, *args, **kwargs):
        return self.params(request, *args, **kwargs)

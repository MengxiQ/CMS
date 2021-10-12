from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class BgpBaseView(ConfigAPIVies):
    # 配置BGP进程
    functionName = '配置BGP进程'


class BgpPeerView(ConfigAPIVies):
    functionName = '配置BGP邻居'

    # def get(self, request, *args, **kwargs):
    #     return self.params(request, *args, **kwargs)


class BgpNetworkView(ConfigAPIVies):
    functionName = '配置BGP路由发布'


class BgpImporProtocol(ConfigAPIVies):
    functionName = '配置BGP引入协议路由'


class BgpImporInstance(ConfigAPIVies):
    functionName = '配置BGP引入实体路由'

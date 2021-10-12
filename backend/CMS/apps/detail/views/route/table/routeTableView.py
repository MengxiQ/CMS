from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class RouteTableView(ConfigAPIVies):
    functionName = '获取基本路由表'

    def get(self, request, *args, **kwargs):
        return self.list(request=request, getConfig=False, *args, **kwargs)

from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class peersTableView(ConfigAPIVies):
    functionName = '获取ospf邻居表'

    def get(self, request, *args, **kwargs):
        return self.list(request, getConfig=False, *args, **kwargs)
from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class ArarmView(ConfigAPIVies):
    functionName = '获取告警列表'

    def get(self, request, *args, **kwargs):
        return self.list(request, getConfig=False, *args, **kwargs)


class BoardResStatesView(ConfigAPIVies):
    functionName = '获取单板资源利用率信息'


class SystemInfoView(ConfigAPIVies):
    functionName = '获取系统信息'
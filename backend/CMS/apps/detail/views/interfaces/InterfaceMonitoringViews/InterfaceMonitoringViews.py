from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class InterfaceMonitoringView(ConfigAPIVies):
    functionName = '接口的监控信息'

    def get(self, request, *args, **kwargs):
        return self.list(request, getConfig=False, *args, **kwargs)
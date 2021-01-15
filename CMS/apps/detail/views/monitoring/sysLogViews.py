from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class SysLogView(ConfigAPIVies):
    functionName = '获取日志缓存区'

    def get(self, request, *args, **kwargs):
        return self.list(request, getConfig=False, *args, **kwargs)
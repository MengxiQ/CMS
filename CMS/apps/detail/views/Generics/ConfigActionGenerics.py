from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class ConfigActionGenerics(ConfigAPIVies):
    def get(self, request, *args, **kwargs):
        return self.list(request, getConfig=False, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, isAction=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, isAction=True, *args, **kwargs)

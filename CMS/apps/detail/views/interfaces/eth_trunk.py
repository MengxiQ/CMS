from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class EthTrunkView(ConfigAPIVies):
    functionName = '配置Eth-Trunk'


class TrunkMemberView(ConfigAPIVies):
    functionName = '配置Eth-Trunk成员接口'

    def get(self, request, *args, **kwargs):
        return self.list(request, getConfig=False, *args, **kwargs)
    # def list(self, request, *args, **kwargs):
    #     """
    #     获取返回配置列表，并返回配置参数列表
    #     """
    #     return self.params(request, *args, **kwargs)

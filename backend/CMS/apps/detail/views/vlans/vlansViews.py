from CMS.apps.detail.views.Generics.ConfigGenerics import ConfigAPIVies


class VlansViews(ConfigAPIVies):
    functionName = '增删改查vlan信息'  # 必要，配置模板的功能名称


class VlanIfView(ConfigAPIVies):
    functionName = '配置vlanif接口'

const getters = {
  // 系统
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  roles: state => state.user.roles,
  permission_routes: state => state.permission.routes,
  // permission_routes: state => state.permission.routes,
  visitedViews: state => state.tagsView.visitedViews,
  cachedViews: state => state.tagsView.cachedViews,
  // 业务
  templateTypes: state => state.types.templateTypes,
  unitTypes: state => state.types.unitTypes,
  functionTypes: state => state.types.functionTypes,
  neTypes: state => state.types.neTypes,
  vendorTypes: state => state.types.vendorTypes,
  // 配置设备的配置
  source: state => state.config.source
}
export default getters

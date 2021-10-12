import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  { // tagView刷新单个页面
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/gohome',
    component: Layout,
    redirect: '/home'
  },
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [{
      path: 'home',
      name: 'Home',
      component: () => import('@/views/home/index'),
      meta: { title: '首页', icon: 'el-icon-s-home' }
    }]
  },

  {
    path: '/equipmentsManage',
    component: Layout,
    redirect: '/equipmentsManage/list',
    name: 'Equipment',
    meta: { title: '设备管理', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'list',
        name: 'EquipmentList',
        component: () => import('@/views/equipmentsManage/list/index'),
        meta: { title: '设备列表', icon: 'el-icon-help' }
      },
      {
        path: 'users',
        name: 'NetconfUser',
        component: () => import('@/views/equipmentsManage/users/index'),
        meta: { title: '设备用户', icon: 'el-icon-s-custom' }
      },
      {
        path: 'batchUsers',
        name: 'BatchUsers',
        component: () => import('@/views/equipmentsManage/batchUser/index'),
        meta: { title: '批量用户', icon: 'el-icon-user-solid' }
      },
      {
        path: 'detail/:ip',
        name: 'Detail',
        redirect: 'detail/:ip/monitoring',
        hidden: true,
        component: () => import('@/views/equipmentsManage/detail/index'),
        meta: { title: '设备详情', showZj: true },
        children: [
          {
            path: 'monitoring',
            name: 'Monitoring',
            redirect: 'monitoring/base',
            component: () => import('@/views/equipmentsManage/detail/components/monitoring/monitoringBase'),
            meta: { title: '监控', showZj: true },
            children: [
              {
                path: 'base',
                name: 'base',
                component: () => import('@/views/equipmentsManage/detail/components/monitoring/components/basePane/basePane'),
                meta: { title: '基本信息', showZj: true }
              },
              {
                path: 'syslog',
                name: 'Syslog',
                component: () => import('@/views/equipmentsManage/detail/components/monitoring/components/syslog/sysLog'),
                meta: { title: '设备日志', showZj: true }
              }]
          },
          {
            path: 'configuration',
            name: 'Configuration',
            redirect: 'configuration/manage',
            component: () => import('@/views/equipmentsManage/detail/components/configuration/configuration'),
            meta: { title: '配置', showZj: true },
            children: [
              {
                path: 'vlan',
                name: 'Vlan',
                redirect: 'vlan/list',
                component: () => import('@/views/equipmentsManage/detail/components/configuration/components/vlanPane/index'),
                meta: { title: 'VLAN配置', showZj: true },
                children: [
                  {
                    path: 'list',
                    name: 'List',
                    component: () => import('@/views/equipmentsManage/detail/components/configuration/components/vlanPane/vlanPane'),
                    meta: { title: '通用接口', showZj: true }
                  }]
              },
              {
                path: 'interface',
                name: 'Interface',
                redirect: 'interface/common',
                component: () => import('@/views/equipmentsManage/detail/components/configuration/components/interfacesPane/index'),
                meta: { title: '接口配置', showZj: true },
                children: [
                  {
                    path: 'monitoring',
                    name: 'interface-monitoring',
                    component: () => import('@/views/equipmentsManage/detail/components/configuration/components/interfacesPane/interfaceMonitoring/list'),
                    meta: { title: '接口监控', showZj: true }
                  },
                  {
                    path: 'common',
                    name: 'Common',
                    component: () => import('@/views/equipmentsManage/detail/components/configuration/components/interfacesPane/commonInterfaces'),
                    meta: { title: '通用接口', showZj: true }
                  },
                  {
                    path: 'ethernet',
                    name: 'Ethernet',
                    component: () => import('@/views/equipmentsManage/detail/components/configuration/components/interfacesPane/ethernetInterfaces'),
                    meta: { title: '以太接口', showZj: true }
                  },
                  {
                    path: 'eth-trunk',
                    name: 'Eth-Trunk',
                    component: () => import('@/views/equipmentsManage/detail/components/configuration/components/interfacesPane/ethTrunk/ethTrunk'),
                    meta: { title: 'Eth-Trunk', showZj: true }
                  }
                ]
              },
              {
                path: 'route',
                name: 'Route',
                redirect: 'route/ospf',
                component: () => import('@/views/equipmentsManage/detail/components/configuration/components/route/index'),
                meta: { title: 'IP路由', showZj: true },
                children: [
                  {
                    path: 'table',
                    name: 'RouteTable',
                    component: () => import('@/views/equipmentsManage/detail/components/configuration/components/route/table/table'),
                    meta: { title: '基本路由表', showZj: true }
                  },
                  {
                    path: 'ospf',
                    name: 'Ospf',
                    component: () => import('@/views/equipmentsManage/detail/components/configuration/components/route/ospf/index'),
                    meta: { title: 'OSPF路由', showZj: true }
                  },
                  {
                    path: 'bgp',
                    name: 'Bgp',
                    component: () => import('@/views/equipmentsManage/detail/components/configuration/components/route/bgpPane/bgpPane'),
                    meta: { title: 'BGP路由', showZj: true }
                  },
                  {
                    path: 'static',
                    name: 'bgp-base',
                    component: () => import('@/views/equipmentsManage/detail/components/configuration/components/route/staticRoutePane/staticRoutePane'),
                    meta: { title: '静态路由', showZj: true }
                  }
                ]
              },
              {
                path: 'manage',
                name: 'Manage',
                redirect: 'manage/setting',
                component: () => import('@/views/equipmentsManage/detail/components/configuration/components/manage/index'),
                meta: { title: '配置管理', showZj: true },
                children: [
                  {
                    path: 'setting',
                    name: 'setting',
                    component: () => import('@/views/equipmentsManage/detail/components/configuration/components/manage/settings/index'),
                    meta: { title: '配置设置', showZj: true }
                  }
                ]
              }
            ]
          },
          {
            path: 'maintain',
            name: 'Maintain',
            component: () => import('@/views/equipmentsManage/detail/components/maintain/maintain'),
            meta: { title: '维护', showZj: true }
          },
          {
            path: 'test',
            name: 'Test',
            redirect: 'test/network',
            component: () => import('@/views/equipmentsManage/detail/components/test/test'),
            meta: { title: '测试', showZj: true },
            children: [
              {
                path: 'network',
                name: 'Test-network',
                component: () => import('@/views/equipmentsManage/detail/components/test/networkTest/index'),
                meta: { title: '网络测试', showZj: true }
              }
            ]
          }
        ]
      },
      // {
      //   path: 'yangTool',
      //   component: () => import('@/views/configManage/yangTool/index'), // Parent router-view
      //   name: 'yangTool',
      //   meta: { title: 'Yang工具', icon: 'nested' }
      // },
      {
        path: 'xmlTool',
        component: () => import('@/views/equipmentsManage/xmlTool/index'), // Parent router-view
        name: 'xmlTool',
        meta: { title: 'XML工具', icon: 'el-icon-s-tools' }
      },
      {
        path: 'batchConfig',
        component: () => import('@/views/equipmentsManage/batchConfig/batchConfig'), // Parent router-view
        name: 'batchConfig',
        meta: { title: '批量配置', icon: 'el-icon-s-open' }
      }
    ]
  },

  {
    path: '/view',
    component: Layout,
    redirect: '/view/topos',
    meta: { title: '视图管理', icon: 'el-icon-guide' },
    children: [
      {
        path: 'topos',
        name: 'Topos',
        component: () => import('@/views/view/topos/index'),
        meta: { title: '拓扑列表', icon: 'el-icon-s-grid' }
      //   children: [
      //     {
      //       path: 'detail/:name',
      //       name: 'viewDetail',
      //       component: () => import('@/views/view/topos/detail/index'),
      //       meta: { title: '拓扑列表', icon: 'el-icon-s-grid' }
      //     }
      //   ]
      },
      {
        path: 'edit',
        name: 'Edit',
        component: () => import('@/views/view/edit/index'),
        meta: { title: '新增视图', icon: 'el-icon-edit-outline' }
      }
    ]
  },
  {
    path: '/templates',
    component: Layout,
    redirect: '/templates/list',
    name: 'Templates',
    alwaysShow: true,
    meta: { title: '模板管理', icon: 'el-icon-s-finance' },
    children: [
      {
        path: 'list',
        component: () => import('@/views/templateManage/templates/list/index'), // Parent router-view
        name: 'Templates-list',
        meta: { title: '模板列表', icon: 'el-icon-s-check' }
      }
      // {
      //   path: 'guideConfig',
      //   component: () => import('@/views/configManage/xmlTool/index'), // Parent router-view
      //   name: 'guideConfig',
      //   meta: { title: '配置向导', icon: 'el-icon-s-tools' }
      // }
    ]
  },

  {
    path: '/types',
    component: Layout,
    alwaysShow: true,
    meta: { title: '类型管理', icon: 'el-icon-receiving' },
    children: [
      {
        path: 'templateTypes',
        name: 'templateTypes',
        component: () => import('@/views/typesManage/templateTypes/index'),
        meta: { title: '模板类型', icon: 'el-icon-takeaway-box' }
      },
      {
        path: 'unitTypes',
        name: 'UnitTypes',
        component: () => import('@/views/typesManage/unitTypes/index'),
        meta: { title: '设备型号', icon: 'el-icon-takeaway-box' }
      },
      {
        path: 'neTypes',
        name: 'NeTypes',
        component: () => import('@/views/typesManage/neTypes/index'),
        meta: { title: '设备类型', icon: 'el-icon-takeaway-box' }
      },
      {
        path: 'functionTypes',
        name: 'FunctionTypes',
        component: () => import('@/views/typesManage/functionTypes/index'),
        meta: { title: '功能列表', icon: 'el-icon-takeaway-box' }
      },
      {
        path: 'vendorTypes',
        name: 'VendorTypes',
        component: () => import('@/views/typesManage/vendorTypes/index'),
        meta: { title: '厂商列表', icon: 'el-icon-takeaway-box' }
      }
    ]
  },
  {
    path: '/system',
    component: Layout,
    alwaysShow: true,
    meta: { title: '系统管理', icon: 'el-icon-s-operation' },
    children: [
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/systemManage/users/index'),
        meta: { title: '系统用户', icon: 'el-icon-s-custom' }
      }
    ]
  },
  {
    path: '/test',
    component: Layout,
    alwaysShow: true,
    meta: { title: '测试页', icon: 'el-icon-s-operation' },
    children: [
      {
        path: 'a',
        name: 'a',
        component: () => import('@/views/test/test'),
        meta: { title: '测试a', icon: 'el-icon-s-custom' }
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()
export const asyncRoutes = []
// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router

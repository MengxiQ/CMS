""" URL Configuration

The `urlpatterns` list routes URLs to viewsManage. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function viewsManage
    1. Add an import:  from my_app import viewsManage
    2. Add a URL to urlpatterns:  path('', viewsManage.home, name='home')
Class-based viewsManage
    1. Add an import:  from other_app.viewsManage import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include

from CMS.apps.detail.views.interfaces.InterfaceMonitoringViews.InterfaceMonitoringViews import InterfaceMonitoringView
from CMS.apps.detail.views.vlans.vlansViews import VlansViews, VlanIfView
from CMS.apps.detail.views.monitoring.monitoring import BoardResStatesView, ArarmView, SystemInfoView
from CMS.apps.detail.views.monitoring.sysLogViews import SysLogView
from CMS.apps.detail.views.manage.commit import CommitView
from CMS.apps.detail.views.route.table.routeTableView import RouteTableView
from CMS.apps.detail.views.testViews.PingTestView import PingTestView
from CMS.apps.detail.views.common.GetNextView import GetNextView
from CMS.apps.detail.views.common.MaintainView import MaintainView
from CMS.apps.detail.views.common.ConnectView import ConnectView
urlpatterns = [
    url(r'config/connect', ConnectView.as_view()),
    url(r'config/vlans', VlansViews.as_view()),
    url(r'config/vlanif', VlanIfView.as_view()),
    url(r'^config/interfaces/', include('CMS.apps.detail.views.interfaces.urls')),
    url(r'^monitoring$', InterfaceMonitoringView.as_view()),
    url(r'^config/monitoring/boardResStates', BoardResStatesView.as_view()),
    url(r'^config/monitoring/alarm', ArarmView.as_view()),
    url(r'^config/monitoring/systemInfo', SystemInfoView.as_view()),
    url(r'^config/monitoring/syslog', SysLogView.as_view()),
    # 配置管理
    url(r'^config/commit$', CommitView.as_view()),
    # 路由配置
    url(r'^config/route/', include('CMS.apps.detail.views.route.urls')),
    # 测试
    url(r'^config/test/ping$', PingTestView.as_view()),
    # 通用方法
    url(r'^config/get/next$', GetNextView.as_view()),  # 获取get-next
    url(r'^config/saveconfig$', MaintainView.as_view()),  # 获取保存配置
]
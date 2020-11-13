""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views.interfacesViews import GatherInterfaces, InterfacesViews
from CMS.apps.detail.views.vlans.vlansViews import VlansViews
from CMS.apps.detail.views.ospf.ospfViews import OspfViews, OspfProcessView, OspfAreaView,\
    OspfAreaNetwork, OspfAdvanceView
from CMS.apps.detail.views.interfaces.common import CommonInterfacesViews
from CMS.apps.detail.views.interfaces.ethernet import EthernetInterfacesViews
from CMS.apps.detail.views.static_route.static import StaticRouteViews
from CMS.apps.detail.views.interfaces.eth_trunk import EthTrunkView, TrunkMemberView
from CMS.apps.detail.views.bgp.bgp_base import BgpBaseView
urlpatterns = [
    url(r'config/gather', GatherInterfaces.as_view()),
    # url(r'config/interfaces', InterfacesViews.as_view()),
    url(r'config/vlans', VlansViews.as_view()),
    url(r'^config/ospf$', OspfViews.as_view()),
    url(r'^config/ospf/process$', OspfProcessView.as_view()),
    url(r'^config/ospf/area$', OspfAreaView.as_view()),
    url(r'^config/ospf/area/network$', OspfAreaNetwork.as_view()),
    url(r'^config/ospf/advance$', OspfAdvanceView.as_view()),
    url(r'^config/interfaces/common$', CommonInterfacesViews.as_view()),
    url(r'^config/interfaces/ethernet$', EthernetInterfacesViews.as_view()),
    url(r'^config/interfaces/eth_trunk$', EthTrunkView.as_view()),
    url(r'^config/static_route$', StaticRouteViews.as_view()),
    url(r'^config/interfaces/eth_trunk/trunk_member$', TrunkMemberView.as_view()),
    url(r'^config/bgp$', BgpBaseView.as_view())
]

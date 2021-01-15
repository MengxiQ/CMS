from django.conf.urls import url

from CMS.apps.detail.views.interfaces.commonInterfaces.l2EnableView import L2EnableView
from CMS.apps.detail.views.interfaces.commonInterfaces.common import CommonInterfacesViews
from CMS.apps.detail.views.interfaces.eth_trunk import EthTrunkView, TrunkMemberView
from CMS.apps.detail.views.interfaces.ethernet import EthernetInterfacesViews
from CMS.apps.detail.views.interfaces.InterfaceMonitoringViews.InterfaceMonitoringViews import InterfaceMonitoringView

urlpatterns = [
    url(r'^monitoring$', InterfaceMonitoringView.as_view()),
    url(r'^common$', CommonInterfacesViews.as_view()),
    url(r'^common/l2Enable$', L2EnableView.as_view()),
    url(r'^ethernet$', EthernetInterfacesViews.as_view()),
    url(r'^eth_trunk$', EthTrunkView.as_view()),
    url(r'^eth_trunk/trunk_member$', TrunkMemberView.as_view()),
]
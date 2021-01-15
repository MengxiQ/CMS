from django.conf.urls import url
from CMS.apps.detail.views.route.bgp.bgp_base import BgpBaseView, BgpPeerView, BgpNetworkView, BgpImporProtocol, \
    BgpImporInstance
from CMS.apps.detail.views.route.ospf.ospfViews import OspfProcessView, OspfAreaView, OspfAreaNetwork, \
    OspfAdvanceView, OspfDefaultAdviseView, OspfImportView
from CMS.apps.detail.views.route.ospf.peersTableView import peersTableView
from CMS.apps.detail.views.route.static_route.static import StaticRouteViews
from CMS.apps.detail.views.route.table.routeTableView import RouteTableView

urlpatterns = [
    url(r'^table$', RouteTableView.as_view()),
    url(r'^ospf/process$', OspfProcessView.as_view()),
    url(r'^ospf/area$', OspfAreaView.as_view()),
    url(r'^ospf/area/network$', OspfAreaNetwork.as_view()),
    url(r'^ospf/advance$', OspfAdvanceView.as_view()),
    url(r'^ospf/advance/import$', OspfImportView.as_view()),
    url(r'^ospf/defaultAdvise$', OspfDefaultAdviseView.as_view()),
    url(r'^ospf/peersTable$', peersTableView.as_view()),
    url(r'^static_route$', StaticRouteViews.as_view()),
    url(r'^bgp$', BgpBaseView.as_view()),
    url(r'^bgp/peer$', BgpPeerView.as_view()),
    url(r'^bgp/network$', BgpNetworkView.as_view()),
    url(r'^bgp/import/protocol', BgpImporProtocol.as_view()),
    url(r'^bgp/import/instance', BgpImporInstance.as_view()),
]
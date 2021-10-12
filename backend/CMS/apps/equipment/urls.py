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
from ..equipment.views.EquipmentViews import EquipmentView, NeTypeView, StatusView, EquipmentByIpView
from ..equipment.views.NetconfUserView import NetconfUserView, BatchUsers
urlpatterns = [
    url(r'^equipment/(?P<pk>[0-9]*)$', EquipmentView.as_view()),
    url(r'equipment/netype/', NeTypeView.as_view()),
    url(r'^equipment/status/(?P<pk>[0-9]*)$', StatusView.as_view()),
    url(r'^equipment/netconfuser/(?P<pk>[0-9]*)$', NetconfUserView.as_view()),
    url(r'^equipment/batchUsers/(?P<pk>[0-9]*)$', BatchUsers.as_view()),
    url(r'^equipment/equipmentByIp/(?P<pk>[0-9]*)$', EquipmentByIpView.as_view())

]

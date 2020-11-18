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
from .views import TempTypesView, UnitTypesView, FunctionsTypesView, \
    NeTypesViews, VendorTypesViews
urlpatterns = [
    url(r'^templateTypes/(?P<pk>[0-9]*)$', TempTypesView.as_view()),
    url(r'^unitTypesTypes/(?P<pk>[0-9]*)$', UnitTypesView.as_view()),
    url(r'^functions/(?P<pk>[0-9]*)$', FunctionsTypesView.as_view()),
    url(r'^neTypes/(?P<pk>[0-9]*)$', NeTypesViews.as_view()),
    url(r'^vendorTypes/(?P<pk>[0-9]*)$', VendorTypesViews.as_view()),
]

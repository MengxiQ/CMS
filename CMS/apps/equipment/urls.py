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
from ..equipment.views.views import Equipment, NeTypeView, StatusView
from ..equipment.views.NetconfUserView import NetconfUserView
urlpatterns = [
    url(r'^equipment/(?P<pk>[0-9]*)$', Equipment.as_view()),
    url(r'equipment/netype/', NeTypeView.as_view()),
    url(r'^equipment/status/(?P<pk>[0-9]*)$', StatusView.as_view()),
    url(r'^equipment/netconfuser/(?P<pk>[0-9]*)$', NetconfUserView.as_view())

]

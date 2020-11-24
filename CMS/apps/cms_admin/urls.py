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
from CMS.apps.cms_admin.views.views import userView
from CMS.apps.cms_admin.views.usersViews import usersView
from CMS.apps.cms_admin.views.statisticalViews import StatisticalViews
urlpatterns = [
    url('^user/$', userView.as_view()),
    url('^users/(?P<pk>[0-9]*)$', usersView.as_view()),
    url('statistica', StatisticalViews.as_view()),
]

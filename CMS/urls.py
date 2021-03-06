"""CMS URL Configuration

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
from django.conf.urls import include
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^admin/', include('CMS.apps.cms_admin.urls')),
    url(r'^asset/', include('CMS.apps.equipment.urls')),
    url(r'^detail/', include('CMS.apps.detail.urls')),
    url(r'^configManage/', include('CMS.apps.configManage.urls')),
    url(r'^typeManage/', include('CMS.apps.typesManage.urls')),
    url(r'^views/', include('CMS.apps.viewsManage.urls')),
]

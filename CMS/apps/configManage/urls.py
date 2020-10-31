from django.conf.urls import url
from CMS.apps.configManage.views.templatesViews import TemplatesViews, TemplateData
urlpatterns = [
    url(r'templates/(?P<pk>[0-9]*)$', TemplatesViews.as_view()),
    url(r'templatesData/(?P<pk>[0-9]*)$', TemplateData.as_view()),
]

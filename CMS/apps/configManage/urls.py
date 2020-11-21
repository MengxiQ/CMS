from django.conf.urls import url
from CMS.apps.configManage.views.templatesViews import TemplatesViews, TemplateData
from CMS.apps.configManage.views.toolsViews import xmlToolView
from CMS.apps.configManage.views.batchConfigViews import GenerateConfig
urlpatterns = [
    url(r'templates/(?P<pk>[0-9]*)$', TemplatesViews.as_view()),
    url(r'templatesData/(?P<pk>[0-9]*)$', TemplateData.as_view()),
    url(r'xmlTools/(?P<pk>[0-9]*)$', xmlToolView.as_view()),
    url(r'GenerateConfig/$', GenerateConfig.as_view()),
]

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from task import views

urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)/status/$', views.TaskResultDetail.as_view(scenario='status')),
    url(r'^(?P<pk>[0-9]+)/result/$', views.TaskResultDetail.as_view(scenario='result')),
    url(r'^(?P<pk>[0-9]+)/$', views.TaskResultDetail.as_view()),
    url(r'^$', views.TaskResultIndex.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='api_index'),
    url(r'^edit/(?P<key_id>\d+)/$', views.key_edit, name='api_key_edit'),
)

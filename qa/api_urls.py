from django.conf.urls import patterns, url

from . import views

# api urls
urlpatterns = patterns('',
    url(r'^search/(?P<apikey>[a-f\d]+)/$', views.search, name='search'),
    url(r'^list/(?P<apikey>[a-f\d]+)/$', views.list_qa, name='list'),
    url(r'^single/(?P<apikey>[a-f\d]+)/$', views.single, name='single'),
    url(r'^rate/(?P<apikey>[a-f\d]+)/$', views.rate, name='rate'),
    url(r'^attachments/(?P<apikey>[a-f\d]+)/$', views.attachments,
        name='attachments'),
)

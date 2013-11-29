from django.conf.urls import patterns, url

from . import views

# api urls
urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),

    url(r'^search/(?P<apikey>[a-f\d]+)/$', views.search, name='search'),
    url(r'^rate/(?P<apikey>[a-f\d]+)/$', views.rate, name='rate'),
)

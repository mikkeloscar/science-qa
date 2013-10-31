from django.conf.urls import patterns, url

from . import views

# api urls
urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),

    url(r'^search/$', views.search, name='search'),
)

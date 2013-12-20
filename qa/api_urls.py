from django.conf.urls import patterns, url

from qa import views

# api urls
urlpatterns = patterns('',
    url(r'^search/(?P<apikey>[a-f\d]+)/$', views.search, name='search'),
    url(r'^list/(?P<apikey>[a-f\d]+)/$', views.list_qa, name='list'),
    url(r'^single/(?P<apikey>[a-f\d]+)/$', views.single, name='single'),
    url(r'^rate/(?P<apikey>[a-f\d]+)/$', views.rate, name='rate'),
    url(r'^attachments/(?P<apikey>[a-f\d]+)/$', views.attachments,
        name='attachments'),
    url(r'^delete_attachment/(?P<apikey>[a-f\d]+)/$', views.delete_attachment,
        name='delete_attachment'),
    url(r'^send_email/(?P<apikey>[a-f\d]+)/$', views.send_email,
        name='send_email'),
)

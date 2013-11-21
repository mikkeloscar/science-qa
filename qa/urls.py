from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^questions/$', views.questions, name='questions'),
    url(r'^questions/add/$', views.question_add, name='question_add'),
    url(r'^questions/(?P<question_uuid>[a-f\d]+)/$', views.question_edit,
        name='question_edit'),
    url(r'^questions/(?P<question_uuid>[a-f\d]+)/delete/$', views.question_delete,
        name='question_delete'),

    url(r'^categories/$', views.categories, name='categories'),
    url(r'^categories/add/$', views.category_add, name='category_add'),
    url(r'^categories/(?P<category_id>\d+)/$', views.category_edit,
        name='category_edit'),
    url(r'^categories/(?P<category_id>\d+)/delete/$', views.category_delete,
        name='category_delete'),

    url(r'^degrees/$', views.degrees, name='degrees'),
    url(r'^degrees/add/$', views.degree_add, name='degree_add'),
    url(r'^degrees/(?P<degree_id>\d+)/$', views.degree_edit,
        name='degree_edit'),
    url(r'^degrees/(?P<degree_id>\d+)/delete/$', views.degree_delete,
        name='degree_delete'),
)

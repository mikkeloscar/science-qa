from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^questions/$', views.questions, name='questions'),
    url(r'^questions/add/$', views.question_add, name='question_add'),
    url(r'^questions/edit/(?P<question_uuid>[a-f\d]+)/$', views.question_edit,
        name='question_edit'),
    url(r'^questions/delete/(?P<question_uuid>[a-f\d]+)/$', views.question_delete,
        name='question_delete'),

    url(r'^categories/$', views.categories, name='categories'),
    url(r'^categories/add/$', views.category_add, name='category_add'),
    url(r'^categories/edit/(?P<category_uuid>\d+)/$', views.category_edit,
        name='category_edit'),
    url(r'^categories/delete/(?P<category_uuid>\d+)/$', views.category_delete,
        name='category_delete'),

    url(r'^degrees/$', views.degrees, name='degrees'),
    url(r'^degrees/add/$', views.degree_add, name='degree_add'),
    url(r'^degrees/edit/(?P<degree_uuid>\d+)/$', views.degree_edit,
        name='degree_edit'),
    url(r'^degrees/delete/(?P<degree_uuid>\d+)/$', views.degree_delete,
        name='degree_delete'),
)

from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('django.contrib.admin',),
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'science_qa.views.home', name='home'),
    # url(r'^science_qa/', include('science_qa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', RedirectView.as_view(url='/qa/questions/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^qa/', include('qa.urls')),
    url(r'^api/', include('qa.api_urls')),
    url(r'^login/', 'django.contrib.auth.views.login', {
        'template_name': 'login.html' }),
    url(r'^logout/', 'django.contrib.auth.views.logout', {
        'template_name': 'logout.html' }),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sigaram.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',          'sigaram.views.home', name='home'),
    url(r'^logout$',    'sigaram.views.logout', name='logout'),
    url(r'^forum$',     'sigaram.views.forum', name='forum'),
    url(r'^siteadmin/', include(admin.site.urls)),
    url(r'^admin/',     include('portaladmin.urls')),
)

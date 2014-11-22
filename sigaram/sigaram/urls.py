from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.utils import translation

translation.activate('ta')

urlpatterns = patterns('',
    url(r'^home$',          'sigaram.views.home', name='home'),
    url(r'^togglelanguage$','sigaram.views.togglelanguage', name='togglelanguage'),
    url(r'^forum$',     'sigaram.views.forum', name='forum'),
    url(r'^siteadmin/', include(admin.site.urls)),
    url(r'^admin/',     include('portaladmin.urls')),
    url(r'^student/',   include('student.urls')),
    url(r'^teacher/',   include('teacher.urls')),
    url(r'^api/admin/',       include('api.urls')),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html'}, name='mysite_login'),
    url(r'^logout/$', 'logout', {'next_page': '/'}, name='mysite_logout'),
)
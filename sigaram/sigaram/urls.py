from django.conf.urls import patterns, include, url
from django.shortcuts import redirect
from django.contrib import admin
from django.http import Http404
from views import Index1View


urlpatterns = patterns('',
    url(r'^$',               Index1View.as_view(),  name='home'), #call back

    url(r'^togglelanguage$','sigaram.views.togglelanguage', name='togglelanguage'),
    url(r'^forum$',     'sigaram.views.forum', name='forum'),
    url(r'^siteadmin/', include(admin.site.urls)),
    url(r'^admin/',     include('portaladmin.urls')),
    url(r'^student/',   include('student.urls')),
    url(r'^teacher/',   include('teacher.urls')),
    url(r'^api/admin/',       include('api.admin.urls')),
    url(r'^api/student/',     include('api.student.urls')),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$',  'login',  {'template_name': 'login.html'}, name='mysite_login'),
    url(r'^logout/$', 'logout', {'next_page': '/login/'}, name='mysite_logout'),
)
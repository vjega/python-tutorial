from django.conf.urls import patterns, include, url
from django.shortcuts import redirect
from django.contrib import admin
from django.http import Http404


urlpatterns = patterns('',
    url(r'^$',              'sigaram.views.home',  name='home'), #call back
    url(r'^togglelanguage$','sigaram.views.togglelanguage', name='togglelanguage'),
    #url(r'^ajax-upload$', 'sigaram.views.import_uploader', name="my_ajax_upload"),
    url(r'^forum/',     include('forum.urls')),
    url(r'^billboard$',     'sigaram.views.billboard', name='forum'),
    url(r'^siteadmin/', include(admin.site.urls)),
    url(r'^admin/',     include('portaladmin.urls')),
    url(r'^student/',   include('student.urls')),
    url(r'^teacher/',   include('teacher.urls')),
    url(r'^forum/',     include('forum.urls')),
    url(r'^api/admin/',       include('api.admin.urls')),
    url(r'^api/student/',     include('api.student.urls')),
    url(r'^api/forum/',     include('api.forum.urls')),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$',  'login',  {'template_name': 'login.html'}, name='mysite_login'),
    url(r'^logout/$', 'logout', {'next_page': '/login/'}, name='mysite_logout'),
)
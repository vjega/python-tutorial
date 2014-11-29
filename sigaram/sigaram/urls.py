from django.conf.urls import patterns, include, url
from django.shortcuts import redirect
from django.contrib import admin
from django.http import Http404

def user_landing(request):
    if str(request.user) == "AnonymousUser": 
        return redirect('/login')
    
    try:
        group = request.user.groups.all()[0].name
    except Exception as e:
        raise(Http404)

    if group == 'Teacher':
        return redirect('/teacher/home')
    elif group == 'Student':
        return redirect('/student/home')
    elif group == 'Admin':
        return redirect('/admin/home')
    else:
        return redirect('/404')

urlpatterns = patterns('',
    url(r'^$',               user_landing,  name='home'), #call back
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
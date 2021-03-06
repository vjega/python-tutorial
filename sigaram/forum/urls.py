#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
#from portaladmin import views

urlpatterns = patterns('forum.views',
    url(r'^$',    'index',name='forum_home'),
    url(r'^home$','index',name='forum_home'),
    url(r'^index$','index',name='index'),
    url(r'^viewtopic$','viewtopic',name='viewtopic'),
    url(r'^viewpost$','viewpost',name='viewpost'),
    url(r'^forum$','forum',name='forum'),
    url(r'^newtopic$','newtopic',name='newtopic'),
)
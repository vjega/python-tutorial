#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from student import views

urlpatterns = patterns('',
    url(r'^home$',                  views.home,         name='home'),
    url(r'^studentresourcetype',    views.studentresourcetype,
                                                        name='studentresourcetype'),
    url(r'^resourcetype',           views.resourcetype, name='resourcetype'),
    url(r'^workspace',              views.workspace,    name='workspace'),
    
)

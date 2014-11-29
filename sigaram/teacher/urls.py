#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
#from teacher import views

urlpatterns = patterns('teacher.views',
    url(r'^home$',                  'home',    name='home'),
    url(r'^assignedresourcelist',   'assignedresourcelist',
                                               name='assignedresourcelist'),
    url(r'^workspace',   'workspace',          name='workspace'),
    url(r'^viewworkspacelist$','viewworkspacelist',
    									        name='viewworkspacelist'),
    url(r'^writtenwork$', 'writtenwork',        name='writtenwork'),
    url(r'^viewassessments$','viewassessments', name='viewassessments'),
    url(r'^adminlist$', 'adminlist', 			name='adminlist'),
    url(r'^teacherslist$','teacherslist', 		name='teacherslist'),
     url(r'^studentslist$','studentslist', 		name='studentslist'),

     
)

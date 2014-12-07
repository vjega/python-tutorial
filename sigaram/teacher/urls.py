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
    url(r'^studentslist','studentslist', 		name='studentslist'),
    url(r'^classroom',   'classroom', 		    name='classroom'),
    url(r'^myprofile',   'myprofile', 		    name='myprofile'),
    url(r'^students',   'students', 		    name='students'),
    url(r'^studentresources','studentresources',name='studentresources'),
    url(r'^studentresourcetype', 'studentresourcetype',
                                                name='studentresourcetype'),
    url(r'^studentresourceunits', 'studentresourceunits',
                                                name='studentresourceunits'),
    url(r'^allschoolresourcelist', 'allschoolresourcelist',    
                                                name='allschoolresourcelist'),
    url(r'^studentresourcelist', 'studentresourcelist',    
                                                name='studentresourcelist'),
    url(r'^assignchapter', 'assignchapter',     name='assignchapter'),
    url(r'^resources', 'resources',             name='resources'),
    url(r'^resource_type', 'resource_type',     name='resource_type'),
    url(r'^allschoolresourcelist', 'allschoolresourcelist', 
                                                name='allschoolresourcelist'),
    url(r'^resource_units', 'resource_units',   name='resource_units'),
    url(r'^resourcelist', 'resourcelist',       name='resourcelist'),
    url(r'^rubrics', 'rubrics',                 name='rubrics'),


    


)

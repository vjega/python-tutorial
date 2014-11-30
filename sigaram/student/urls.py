#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from student import views

urlpatterns = patterns('student.views',
    url(r'^home$',                      'home',         name='home'),
    url(r'^studentresourcetype',        'studentresourcetype',
                                                        name='studentresourcetype'),
    url(r'^resourcetype',               'resourcetype', name='resourcetype'),
    url(r'^workspace',                  'workspace',    name='workspace'),
    url(r'^studentslist',               'studentslist', name='studentslist'),
    url(r'^assignedresourcelist',  	    'assignedresourcelist',  
                                                        name='assignedresourcelist'),
    url(r'^studentprofile',  		    'studentprofile',  
                                                        name='studentprofile'),
    url(r'^studentassignedresourcelist','studentassignedresourcelist',  
                                                        name='studentassignedresourcelist'),
    url(r'^viewstudentresource',        'viewstudentresource',  
                                                        name='viewstudentresource'),
    
)

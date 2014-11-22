#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from student import views

<<<<<<< HEAD
urlpatterns = patterns('student.views',
    url(r'^home$',                  'home',         name='home'),
    url(r'^studentresourcetype',    'studentresourcetype',
                                                    name='studentresourcetype'),
    url(r'^resourcetype',           'resourcetype', name='resourcetype'),
    url(r'^workspace',              'workspace',    name='workspace'),
    url(r'^studentslist',           'studentslist', name='studentslist'),
=======
urlpatterns = patterns('',
    url(r'^home$',                  views.home,         name='home'),
    url(r'^studentresourcetype',    views.studentresourcetype,
                                                        name='studentresourcetype'),
    url(r'^resourcetype',           views.resourcetype, name='resourcetype'),
    url(r'^workspace',              views.workspace,    name='workspace'),
    
>>>>>>> fe1a06012985c260f6f2f5f3a40ad0ac6d72cb2f
)

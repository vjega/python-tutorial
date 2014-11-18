#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from portaladmin import views

urlpatterns = patterns('',
    url(r'^home$',                    views.home,         name='home'),
    url(r'^adminlist$',               views.adminlist,    name='adminlist'),
    url(r'^teacherslist$',            views.teacherslist, name='teacherslist'),
    url(r'^studentslist$',            views.studentslist, name='studentslist'),
    url(r'^schoollist$',              views.schoollist,   name='schoollist'),
    url(r'^teacherresourcelist$',     views.teacherresourcelist,
                                                          name='teacherresourcelist'),
    url(r'^studentresourcetype',      views.studentresourcetype,
                                                          name='studentresourcetype'),
    url(r'^resourcetype',             views.resourcetype, name='resourcetype'),
    url(r'^subjectlist',              views.subjectlist,  name='subjectlist'),
    url(r'^classlist',                views.classlist,    name='classlist'),
    #url(r'^extras',                   views.extras,       name='extras'),
    #url(r'^statisticsstudentslist$',  views.statisticsstudentslist,
    #                                                      name='statisticsstudentslist'),
    url(r'^statistics-activities$',   views.statistics,   name='statistics'),
    url(r'^statistics-assignment$',   views.statistics,   name='statistics'),
    url(r'^statistics-assessment$',   views.statistics,   name='statistics'),
    url(r'^classroom$',               views.classroom,    name='classroom'),
    url(r'^billboard$',               views.billboard,    name='billboard'),
    url(r'^mindmap$',                 views.mindmap,    name='mindmap'),
    url(r'^sticky_notes$',            views.sticky_notes,    name='sticky_notes'),
    url(r'^calendar$',                views.calendar,    name='calendar'),
    #(r'^api/', include(v1_api.urls)),
)

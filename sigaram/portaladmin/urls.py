#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from portaladmin import views
urlpatterns = patterns('',
    url(r'^home$',                    views.home,         name='home'),
    url(r'^adminlist$',               views.adminlist,    name='adminlist'),
    url(r'^teacherslist$',            views.teacherslist, name='teacherslist'),
    url(r'^studentslist',             views.studentslist, name='studentslist'),
    url(r'^schoollist',               views.schoollist,   name='schoollist'),
    url(r'^teacherresourcelist',      views.teacherresourcelist,
                                                          name='teacherresourcelist'),
    url(r'^statisticsstudentslist',   views.statisticsstudentslist,
                                                          name='statisticsstudentslist'),
    url(r'^statistics-activities',    views.statistics,   name='statistics'),
    url(r'^statistics-assignment',    views.statistics,   name='statistics'),
    url(r'^statistics-assessment$',   views.statistics,   name='statistics'),
    url(r'^classroom$',               views.classroom,    name='classroom'),
    url(r'^billboard$',               views.billboard,    name='billboard'),
)

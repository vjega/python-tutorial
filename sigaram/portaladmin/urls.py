#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
#from portaladmin import views

urlpatterns = patterns('portaladmin.views',
    url(r'^home$',                    'home',         name='home'),
    url(r'^adminlist$',               'adminlist',    name='adminlist'),
    url(r'^teacherslist$',            'teacherslist', name='teacherslist'),
    url(r'^studentslist$',            'studentslist', name='studentslist'),
    url(r'^schoollist$',              'schoollist',   name='schoollist'),
    url(r'^teacherresourcelist$',     'teacherresourcelist',
                                                    name='teacherresourcelist'),
    url(r'^studentresourcetype',      'studentresourcetype',
                                                    name='studentresourcetype'),
    url(r'^resourcetype',             'resourcetype', name='resourcetype'),
    url(r'^subjectlist',              'subjectlist',  name='subjectlist'),
    url(r'^classlist',                'classlist',    name='classlist'),
    #url(r'^extras',                   views.'extras',       name='extras'),
    #url(r'^statisticsstudentslist$',  views.'statisticsstudentslist',
    #                                                      name='statisticsstudentslist'),
    url(r'^statistics-activities$',   'statistics',   name='statistics'),
    url(r'^statistics-assignment$',   'statistics',   name='statistics'),
    url(r'^statistics-assessment$',   'statistics',   name='statistics'),
    url(r'^classroom$',               'classroom',    name='classroom'),
    url(r'^billboard$',               'billboard',    name='billboard'),
    url(r'^mindmap$',                 'mindmap',    name='mindmap'),
    url(r'^sticky_notes$',            'sticky_notes',    name='sticky_notes'),
    url(r'^calendar$',                'calendar',    name='calendar'),
    #(r'^api/', include(v1_api.urls)),
)

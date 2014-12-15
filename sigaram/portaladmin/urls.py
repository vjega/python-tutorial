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
    url(r'^viewteacherresource$',     'viewteacherresource',
                                                    name='viewteacherresource'),
    url(r'^studentresourcetype',      'studentresourcetype',
                                                      name='studentresourcetype'),
    url(r'^studentprofile',           'studentprofile',
                                                      name='studentprofile'),
    url(r'^studentresourcelist',      'studentresourcelist',
                                                      name='studentresourcelist'),
    url(r'^resourcetype',             'resourcetype', name='resourcetype'),
    url(r'^subjectlist',              'subjectlist',  name='subjectlist'),
    url(r'^classlist',                'classlist',    name='classlist'),
    url(r'^chapterlist',              'chapterlist',  name='chapterlist'),
    url(r'^viewstudentresourcelist',  'viewstudentresourcelist',  
                                                      name='viewstudentresourcelist'),
    url(r'^viewstudentwrittenworks',  'viewstudentwrittenworks',  
                                                      name='viewstudentwrittenworks'),
       
    #url(r'^extras',                   views.'extras',       name='extras'),
    #url(r'^statisticsstudentslist$',  views.'statisticsstudentslist',
    url(r'^statistics-activities$',   'statistics',   name='statistics'),
    url(r'^statistics-assignment$',   'statistics',   name='statistics'),
    url(r'^statistics-assessment$',   'statistics',   name='statistics'),
    url(r'^classroom$',               'classroom',    name='classroom'),
    url(r'^billboard$',               'billboard',    name='billboard'),
    url(r'^mindmapedit$',             'mindmapedit',  name='mindmap'),
    url(r'^mindmaplist$',             'mindmaplist',  name='mindmapnew'),
    url(r'^sticky_notes$',            'sticky_notes', name='sticky_notes'),
    url(r'^calendar$',                'calendar',     name='calendar'),
    url(r'^recorder$',                'recorder',     name='recorder'),
    url(r'^studentassignedresourcelist',
                                      'studentassignedresourcelist',
                                                      name='studentassignedresourcelist'),
    url(r'^viewstudentwork',
                                      'viewstudentwork',
                                                      name='viewstudentwork'),
    #(r'^api/', include(v1_api.urls)),
)

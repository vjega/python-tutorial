#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
#from teacher import views

urlpatterns = patterns('teacher.views',
    url(r'^home$',                  'home',             name='home'),
    url(r'^assignedresourcelist$',   'assignedresourcelist',
                                                        name='assignedresourcelist'),
    #url(r'^workspace',         'workspace',          name='workspace'),
    url(r'^viewworkspacelist$',     'viewworkspacelist',
                                                        name='viewworkspacelist'),
    url(r'^writtenwork$',           'writtenwork',      name='writtenwork'),
    url(r'^viewassessments$',       'viewassessments',  name='viewassessments'),
    url(r'^adminlist$',             'adminlist',        name='adminlist'),
    url(r'^teacherslist$',          'teacherslist',     name='teacherslist'),
    url(r'^studentslist$',          'studentslist',     name='studentslist'),
    url(r'^classroom$',             'classroom',        name='classroom'),
    url(r'^myprofile$',             'myprofile',        name='myprofile'),
    url(r'^students$',              'students',         name='students'),
    url(r'^studentresources$',      'studentresources', name='studentresources'),
    url(r'^studentresourcetype$',   'studentresourcetype',
                                                        name='studentresourcetype'),
    url(r'^studentresourceunits$',  'studentresourceunits',
                                                        name='studentresourceunits'),
    url(r'^extras$',                'extras',           name='extras'),
    url(r'^extraslist$',            'extraslist',       name='extraslist'),
    url(r'^allschoolresourcelist$', 'allschoolresourcelist',    
                                                        name='allschoolresourcelist'),
    url(r'^studentresourcelist$',   'studentresourcelist',    
                                                        name='studentresourcelist'),
    url(r'^assignchapter$',         'assignchapter',    name='assignchapter'),
    url(r'^resources$',             'resources',        name='resources'),
    url(r'^resource_type$',         'resource_type',    name='resource_type'),
    url(r'^resource_units$',        'resource_units',   name='resource_units'),
    url(r'^assignresource$',        'assignresource',   name='assignresource'),
    url(r'^resource_units$',        'resource_units',   name='resource_units'),
    url(r'^resourcelist$',          'resourcelist',     name='resourcelist'),
    url(r'^rubrics$',               'rubrics',          name='rubrics'),
    url(r'^statistics$',            'statistics',       name='statistics'),
    url(r'^statisticsstudentslist$','statisticsstudentslist',
                                                        name='statisticsstudentslist'),
    url(r'^rubric_edit$',           'rubric_edit',      name='rubric_edit'),
    url(r'^rubric_view$',           'rubric_view',      name='rubric_view'),
    url(r'^viewassignresource$',     'viewassignresource',  
                                                        name='viewassignresource'),
    url(r'^viewassignmentanswer$',   'viewassignmentanswer',  
                                                        name='viewassignmentanswer'),
    url(r'^mindmaplist$',               'mindmaplist',  name='mindmapnew'),
    url(r'^sticky-notes$',          'stickynotes',      name='stickynotes'),
    url(r'^billboard$',             'billboard',        name="billboard"),
    url(r'^activitystatistics$',    'activitystatistics',     
                                                        name="activitystatistics"),
    url(r'^topics$',                'topics',           name="topics"),
    url(r'^addwrittenwork$',        'addwrittenwork',     
                                                        name="addwrittenwork"),
    url(r'^thread$',                'thread',           name="thread"),
    url(r'^threadview$',            'threadview',       name="threadview"),
    url(r'^bulletinboardlist$',     'bulletinboardlist',           
                                                        name="bulletinboardlist"),
    url(r'^bulletinboard$',             'bulletinboard', name="bulletinboard"),
    url(r'^studentprofile$',        'studentprofile',   name='studentprofile'),
    url(r'^studentassignedresourcelist$',   'studentassignedresourcelist',  
                                                        name='studentassignedresourcelist'),
    url(r'^viewstudentwrittenworks$',       'viewstudentwrittenworks',  
                                                            name='viewstudentwrittenworks'),

    url(r'^sticky-notes-list$',   'stickynoteslist',      name='stickynoteslist'),
    url(r'^forum$','forum',name='forum'),
    url(r'^viewtopic$','viewtopic',name='viewtopic'),
    url(r'^viewpost$','viewpost',name='viewpost'),
    url(r'^newtopic$','newtopic',name='newtopic'),
    url(r'^billviewassignmentanswer$',  'billviewassignmentanswer', 
                                                         name="billviewassignmentanswer"),
    url(r'^bulletinboard-upload$',      'bulletinboard_uploader', 
                                                         name="bulletinboard-uploader"),
    url(r'^viewbulletinboard$',          'viewbulletinboard', 
                                                         name="viewbulletinboard"),
    url(r'^viewassignwrittenwork$',  'viewassignwrittenwork', 
                                                         name="viewassignwrittenwork"),
    url(r'^viewteacherresource$',     'viewteacherresource',
                                                        name='viewteacherresource'),
    url(r'^viewassignwrittenworkanswer$',   'viewassignwrittenworkanswer',  
                                                            name='viewassignwrittenworkanswer'),
    url(r'^viewmyresourcelist$', 'viewmyresourcelist',  
                                                         name='viewmyresourcelist'),
    url(r'^myresourcelist$',           'myresourcelist', 
                                                         name="myresourcelist"),
)

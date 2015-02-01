#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
#from student import views

urlpatterns = patterns('student.views',
    url(r'^home$',                          'home',         name='home'),
    url(r'^studentresourcetype$',           'studentresourcetype',
                                                            name='studentresourcetype'),
    url(r'^resourcetype$',                  'resourcetype', name='resourcetype'),
    url(r'^workspace$',                     'workspace',    name='workspace'),
    url(r'^studentslist$',                  'studentslist', name='studentslist'),
    url(r'^assignedresourcelist$',  	    'assignedresourcelist',  
                                                            name='assignedresourcelist'),
    url(r'^studentprofile$',  		        'studentprofile',  
                                                            name='studentprofile'),
    url(r'^studentassignedresourcelist$',   'studentassignedresourcelist',  
                                                            name='studentassignedresourcelist'),
    url(r'^viewstudentresource$',           'viewstudentresource',  
                                                            name='viewstudentresource'),
    url(r'^viewstudentwrittenworks$',       'viewstudentwrittenworks',  
                                                            name='viewstudentwrittenworks'),
    url(r'^viewstudentwork$',               'viewstudentwork',  
                                                            name='viewstudentwork'),
    url(r'^worklistinfo$',                  'worklistinfo',  
                                                            name='worklistinfo'),
    url(r'^studentviewwork$',               'studentviewwork',  
                                                            name='studentviewwork'),
    url(r'^studentnoteslist$',              'studentnoteslist',  
                                                            name='studentnoteslist'),
    url(r'^studentwrittenwork$',            'studentwrittenwork',  
                                                            name='studentwrittenwork'),
    url(r'^studentviewassessments$',        'studentviewassessments',  
                                                            name='studentviewassessments'),
    url(r'^classroom$',                     'classroom',  
                                                            name='classroom'),
    url(r'^viewassignresource$',            'viewassignresource',  
                                                            name='viewassignresource'),
    url(r'^viewassignmentanswer',           'viewassignmentanswer',   
                                                            name='viewassignmentanswer'),
    url(r'^sticky-notes$',                  'stickynotes',  name='stickynotes'),
    url(r'^billboard$',                     'billboard',    name='billboard'),
    url(r'^billviewassignmentanswer$',      'billviewassignmentanswer',  
                                                            name='billviewassignmentanswer'),
    url(r'^bulletinboardlist$',             'bulletinboardlist',   
                                                            name='bulletinboardlist'),
    url(r'^studentresourceunits$',          'studentresourceunits',   
                                                            name='studentresourceunits'),
    url(r'^studentresourcelist$',           'studentresourcelist',   
                                                            name='studentresourcelist'),
    url(r'^topics$',                        'topics',       name='topics'),
    url(r'^sticky-notes-list$',             'stickynoteslist',      
                                                            name='stickynoteslist'),
    url(r'^viewbulletinboard$',             'viewbulletinboard', 
                                                            name="viewbulletinboard"),
    url(r'^bulletinboard-upload$',          'bulletinboard_uploader', 
                                                            name="bulletinboard-uploader"),
    url(r'^viewassignwrittenwork$',         'viewassignwrittenwork',  
                                                            name='viewassignwrittenwork'),
    url(r'^viewassignwrittenworkanswer$',   'viewassignwrittenworkanswer',  
                                                            name='viewassignwrittenworkanswer'),
    url(r'^classviewassignmentanswer',      'classviewassignmentanswer',   
                                                            name='classviewassignmentanswer'),
    url(r'^classviewassignwrittenworkanswer$', 'classviewassignwrittenworkanswer',  
                                                            name='classviewassignwrittenworkanswer'),
    url(r'^sturesourcetype$', 'sturesourcetype',  
                                                            name='sturesourcetype'),
    url(r'^studentviewmindmap$', 'studentviewmindmap',  
                                                            name='studentviewmindmap'),
    url(r'^viewassignmindmap$', 'viewassignmindmap',  
                                                            name='viewassignmindmap'),
    url(r'^viewassignmindmapanswer$', 'viewassignmindmapanswer',  
                                                            name='viewassignmindmapanswer'), 
    url(r'^viewtopic$',                 'viewtopic',        name='viewtopic'),
    url(r'^viewpost$',                  'viewpost',         name='viewpost'),
    url(r'^newtopic$',                  'newtopic',         name='newtopic')   
)
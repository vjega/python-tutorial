#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
#from portaladmin import views

urlpatterns = patterns('portaladmin.views',
    url(r'^home$',                    'home',           name='home'),
    url(r'^adminlist$',               'adminlist',      name='adminlist'),
    url(r'^teacherslist$',            'teacherslist',   name='teacherslist'),
    url(r'^studentslist$',            'studentslist',   name='studentslist'),
    url(r'^schoollist$',              'schoollist',     name='schoollist'),
    url(r'^teacherresourcelist$',     'teacherresourcelist',
                                                        name='teacherresourcelist'),
    url(r'^viewteacherresource$',     'viewteacherresource',
                                                        name='viewteacherresource'),
    url(r'^studentresourcetype$',      'studentresourcetype',
                                                        name='studentresourcetype'),
    url(r'^studentprofile$',           'studentprofile',
                                                        name='studentprofile'),
    url(r'^studentresourcelist$',      'studentresourcelist',
                                                        name='studentresourcelist'),
    url(r'^resourcetype$',             'resourcetype',  name='resourcetype'),
    url(r'^subjectlist$',              'subjectlist',   name='subjectlist'),
    url(r'^classlist$',                'classlist',     name='classlist'),
    url(r'^chapterlist$',              'chapterlist',   name='chapterlist'),
    url(r'^viewstudentresourcelist$',  'viewstudentresourcelist',  
                                                        name='viewstudentresourcelist'),
    url(r'^viewstudentwrittenworks$',  'viewstudentwrittenworks',  
                                                        name='viewstudentwrittenworks'),
       
    #url(r'^extras',                   views.'extras',       name='extras'),
    #url(r'^statisticsstudentslist$',  views.'statisticsstudentslist',
    url(r'^statistics-activities$',     'statistics',   name='statistics'),
    url(r'^statistics-assignment$',     'statisticsassignment',  
                                                        name='statisticsassignment'),
    url(r'^statistics-assessment$',     'statisticsassessment',   name='statisticsassessment'),
    url(r'^classroom$',                 'classroom',    name='classroom'),
    url(r'^billboard$',                 'billboard',    name='billboard'),
    url(r'^mindmapedit$',               'mindmapedit',  name='mindmap'),
    url(r'^mindmaplist$',               'mindmaplist',  name='mindmapnew'),
    url(r'^sticky-notes$',              'stickynotes',  name='stickynotes'),
    url(r'^calendar$',                  'calendar',     name='calendar'),
    url(r'^recorder$',                  'recorder',     name='recorder'),
    url(r'^studentassignedresourcelist$','studentassignedresourcelist',
                                                        name='studentassignedresourcelist'),
    url(r'^viewstudentwork$',            'viewstudentwork',             
                                                        name='viewstudentwork'),
    url(r'^admin-img-upload$',          'admin_img_uploader',          
                                                        name="admin_ajax_upload"),
    url(r'^teacher-img-upload$',        'teacher_img_uploader',         
                                                        name="teacher_ajax_upload"),
    url(r'^student-img-upload$',        'student_img_uploader',         
                                                        name="student-img-upload"),
    url(r'^student-studentres-upload$', 'student_studentres_uploader',  
                                                        name="student-studentres-upload"),
    url(r'^student-teacherres-upload$', 'student_teacherres_uploader', 
                                                         name="student-teacherres-uploader"),
    url(r'^bulletinboardlist$',         'bulletinboardlist',           
                                                         name="bulletinboardlist"),
    url(r'^bulletinboard$',             'bulletinboard', name="bulletinboard"),
    url(r'^layoutdemo$',                'layoutdemo',    name="layoutdemo"),
    url(r'^billboard$',                 'billboard',     name="billboard"),

    url(r'^billviewassignmentanswer$',  'billviewassignmentanswer', 
                                                         name="billviewassignmentanswer"),
    url(r'^billviewwrittenworkanswer$', 'billviewwrittenworkanswer', 
                                                         name="billviewwrittenworkanswer"),
    url(r'^billfillinganswerrating$',   'billfillinganswerrating',    
                                                         name="billfillinganswerrating"),
    url(r'^billchooseanswerrating$',    'billchooseanswerrating', 
                                                         name="billchooseanswerrating"),
    url(r'^billcomprehensionanswerrating$', 'billcomprehensionanswerrating',
                                                         name="billcomprehensionanswerrating"),
    url(r'^billopenendedanswerrating$', 'billopenendedanswerrating',
                                                         name="billopenendedanswerrating"),
    url(r'^bulletinboard-upload$',      'bulletinboard_uploader', 
                                                         name="bulletinboard-uploader"),
    url(r'^sticky-notes-list$',        'stickynoteslist',     name='stickynoteslist'),
    url(r'^topics$',                   'topics',        name='topics'),
    url(r'^writtenwork-upload$',      'writtenwork_uploader', 
                                                        name="writtenwork-uploader"),
    url(r'^myresourcelist$',           'myresourcelist', 
                                                        name="myresourcelist"),
    url(r'^viewbulletinboard$',          'viewbulletinboard', 
                                                        name="viewbulletinboard"),
    url(r'^resources$',                 'resources',        name='resources'),
    url(r'^classviewassignmentanswer$', 'classviewassignmentanswer',  
                                                        name='classviewassignmentanswer'),
    url(r'^viewmyresourcelist$', 'viewmyresourcelist',  
                                                        name='viewmyresourcelist'),
    url(r'^classviewassignwrittenworkanswer$', 'classviewassignwrittenworkanswer',  
                                                        name='classviewassignwrittenworkanswer'),
    url(r'^rubrics$',                   'rubrics',          name='rubrics'),
    url(r'^viewteacherres$',            'viewteacherres',  name='viewteacherres'),
    url(r'^viewstudentres$',            'viewstudentres',  name='viewstudentres'),
    url(r'^addstickynote$',             'addstickynote',    name='addstickynote'),
    url(r'^summernote_image_test$',     'summernote_image_test',    
                                                        name='summernote_image_test'),
    url(r'^rubric-upload$',             'rubric_uploader', 
                                                        name="rubric-uploader"), 
    url(r'^viewtopic$',                 'viewtopic',      name='viewtopic'),
    url(r'^viewpost$',                  'viewpost',       name='viewpost'),
    url(r'^newtopic$',                  'newtopic',       name='newtopic'),
    url(r'^sticky_notes_upload$', 'sticky_notes_uploader', 
                                                        name="sticky_notes_uploader"),
    url(r'^activitystatistics$', 'activitystatistics', 
                                                         name="activitystatistics"), 
    url(r'^richmindmap$', 'richmindmap', name="richmindmap"),
    url(r'^rubric_view$', 'rubric_view', name="rubric_view"),
    url(r'^billboardviewassignwrittenworkanswer$',   'billboardviewassignwrittenworkanswer',  
                                                name='billboardviewassignwrittenworkanswer'),   
    url(r'^assignmentstatistics$',  'assignmentstatistics', name="assignmentstatistics"),
    url(r'^activityassignment$', 'activityassignment', 
                                                         name="activityassignment"), 
    url(r'^activityassessment$', 'activityassessment', 
                                                         name="activityassessment"), 
    url(r'^billboardviewassignmentanswer$', 'billboardviewassignmentanswer', 
                                                         name="billboardviewassignmentanswer"), 
   
    #(r'^api/', include(v1_api.urls)),
)
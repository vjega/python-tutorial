# -*- coding: utf-8 -*-
from django.utils.translation import (ugettext as _, activate)
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from teacher import models
from portaladmin import models as models
from teacher.forms import ( RubricsForm,
                            StudentForm,
                            StickyForm,
                            StickyCommentForm,
                            TeacherResourceForm,
                            ForumForm,
                            ThreadForm,
                            AnnouncementForm,
                            StickyinfoForm,
                            NewtopicForm,
                            MyprofileForm,
                            MyresourcelistForm
                            ) 

from ajaxuploader.views import AjaxFileUploader  

def switchlanguage(f):
    def inner(req):
        activate(req.session.get('django_language','ta'))
        return f(req)
    return inner

admin_img_uploader = AjaxFileUploader(UPLOAD_DIR='static/admins', 
                                      #backend=EasyThumbnailUploadBackend, 
                                      DIMENSIONS=(250, 250))
teacher_img_uploader = AjaxFileUploader(UPLOAD_DIR='static/teachers', 
                                      #backend=EasyThumbnailUploadBackend, 
                                      DIMENSIONS=(250, 250))

student_img_uploader = AjaxFileUploader(UPLOAD_DIR='static/teachers', 
                                      #backend=EasyThumbnailUploadBackend, 
                                      DIMENSIONS=(250, 250))

bulletinboard_uploader = AjaxFileUploader(UPLOAD_DIR='static/bulletinboard')

@login_required
@switchlanguage
def home(request):
    folders = [{
        "color": u"primary",
        "icon" : u"file-text-o",
        "link" : u"assignedresourcelist",
        "caption": _("Assignment"),
        "stat": 25
        },{
        "color": u"green",
        "icon" : u"pencil-square-o",
        "link" : u"writtenwork",
        "caption":_("Written Work"),
        "stat": 125
        },{
        "color": u"red",
        "icon" : u"pencil",
        "link" : u"viewassessments",
        "caption": _("Exercises"),
        "stat": 125
        },
        {
        "color": u"primary",
        "icon" : u"sitemap",
        "link" : u"teacherviewmindmap",
        "caption": _("Mindmap"),
        "stat": 125
        }]

    recent_acitivity_head = [_("Sl No."),
                             _("Activities"),
                             _("Date")]
    admin_folders = models.AdminFolders.folders(request)
    announcement_body = models.Bulletinboardinfo.announcement(request)
    recent_activity_body = models.Activitylog.recentactivities()
    recent_activities = {'head':recent_acitivity_head,
                         'body':recent_activity_body}
    announcement = {'body':announcement_body}
    return  render(request, 'portalteacher/index.html', {"folders":folders,
                                           "admin_folders":admin_folders,
                                           "recent_activities":recent_activities,
                                           "announcement":announcement
                                           })

@login_required
@switchlanguage
def assignedresourcelist(request):
    return render(request, 'portalteacher/assignedresourcelist.html')


@login_required
@switchlanguage
def viewworkspacelist(request):
   # print request.GET.get('type')
    return render(request, 'portalteacher/viewworkspacelist.html', {'opt':request.GET.get('type'),
                                                 "form" : ViewworkspaceForm.ViewworkspaceForm()})

@login_required
@switchlanguage
def writtenwork(request):
    return render(request, 'portalteacher/writtenwork.html')
@login_required
@switchlanguage
def viewassessments(request):
    return render(request, 'portalteacher/viewassessments.html')

@login_required
@switchlanguage
def adminlist(request):
    return render(request, 'portalteacher/adminlist.html')

@login_required
@switchlanguage
def teacherslist(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/teacherslist.html', 
                                        {'schools':schools,'classes':classes})

@login_required
@switchlanguage
def studentslist(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/studentslist.html', {'schools':schools,
                                    'classes':classes,"form" : StudentForm.StudentForm()})
                                                             

@login_required
@switchlanguage
def classroom(request):
    return render(request, 'portalteacher/classroom.html')

@login_required
@switchlanguage
def myprofile(request):
    return render(request, 'portalteacher/myprofile.html',{'form':MyprofileForm.MyprofileForm()})

@login_required
@switchlanguage
def students(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/students.html', {'schools':schools,
                                                             'classes':classes})


@login_required
@switchlanguage
def studentresources(request):
    folders = [{
        "id": "p1",
        "name" :"P1"
        },{
        "id": "p2",
        "name" :"P2"
        },{
        "id": "p3",
        "name" :"P3"
        },{
        "id": "p4",
        "name" :"P4"
        },{
        "id": "p5",
        "name" :"P5"
        },{
        "id": "p6",
        "name" :"P6"
        },{
        "id": "s1",
        "name" :"S1"
        },{
        "id": "s2",
        "name" :"S2"
        },{
        "id": "s3",
        "name" :"S3"
        },{
        "id": "s4",
        "name" :"S4"
        }
        ]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalteacher/studentresources.html', 
                  {"folders":folders,'studentresources':studentresources})

@login_required
@switchlanguage
def studentresourcetype(request):
    folders = [{
        "id": "1",
        "categoryid": "0",
        "name" :_("Reading"),
        "href" :"studentresourceunits"
        },{
        "id": "2",
        "categoryid": "1",
        "name" :_("Animation"),
        "href" :"studentresourceunits"
        },{
        "id": "3",
        "categoryid": "2",
        "name" :_("Writing board"),
        "href" :"studentresourceunits"
        },{
        "id": "4",
        "name" :_("Composition"),
        "href" :"extras"
        },{
        "id": "5",
        "categoryid": "4",
        "name" :_("Mindmap"),
        "href" :"studentmindmaplist"        
        }]
    classid = request.GET.get('classid')
    section = request.GET.get('section')
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalteacher/studentresourcetype.html', 
                  {"folders":folders,
                  "studentresourcetype":studentresourcetype,
                  "classid":classid,
                  "section":section}
                  )

@login_required
@switchlanguage
def extras(request):
    folders = [{
        "id": "1",
        "type": "text",
        "name" :_("writing"),
        "href" :"extraslist"
        },{
        "id": "2",
        "type": "image",
        "name" :_("Multimedia"),
        "href" :"extraslist"
        },{
        "id": "3",
        "type": "audio",
        "name" :_("Songs"),
        "href" :"extraslist"
        },{
        "id": "4",
        "type": "video",
        "name" :_("Olippatakkatci"),
        "href" :"extraslist"
        }]
    classid = request.GET.get('classid')
    section = request.GET.get('section')
    return render(request, 'portalteacher/extras.html', 
                  {'folders':folders,'classid':classid,
                    'section':section})

@login_required
@switchlanguage
def studentresourceunits(request):
    #studentresourceunits_body = models.Chapterinfo.objects.all()
    return render(request, 
                  'portalteacher/studentresourceunits.html', 
                  {'studentresourceunits':studentresourceunits,
                   'classid': request.GET.get('classid'),
                   'section': request.GET.get('section')    
                  })

@login_required
@switchlanguage
def studentresourcelist(request):
    return render(request, 'portalteacher/studentresourcelist.html', 
                    {'studentresourcelist':studentresourcelist}) 

@login_required
@switchlanguage
def assignchapter(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/assignchapter.html', 
                    {'assignchapter':assignchapter,'schools':schools,
                                             'classes':classes   }) 

@login_required
@switchlanguage
def assignresource(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/assignresource.html', 
                    {'assignresource':assignresource,'schools':schools,
                                             'classes':classes   })

@login_required
@switchlanguage
def resources(request):
    folders = [{
        "id": "2",
        "categoryid": "1",
        "name" :_("Lesson Plans"),
        "href" :"resource_type"
        },{
        "id": "3",
        "categoryid": "2",
        "name" :_("Teacher Share"),
        "href" :"allschoolresourcelist"
        }]

    return render(request, 'portalteacher/resources.html', 
                  {"folders":folders,'resources':resources})

@login_required
@switchlanguage
def resource_type (request):
    folders = [{
        "id": "p1",
        "name" :"P1"
        },{
        "id": "p2",
        "name" :"P2"
        },{
        "id": "p3",
        "name" :"P3"
        },{
        "id": "p4",
        "name" :"P4"
        },{
        "id": "p5",
        "name" :"P5"
        },{
        "id": "p6",
        "name" :"P6"
        },{
        "id": "s1",
        "name" :"S1"
        },{
        "id": "s2",
        "name" :"S2"
        },{
        "id": "s3",
        "name" :"S3"
        },{
        "id": "s4",
        "name" :"S4"
        }
        ]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalteacher/resource_type.html', 
                  {"folders":folders,'resource_type':resource_type})


@login_required
@switchlanguage
def allschoolresourcelist(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/allschoolresourcelist.html', 
                                        {'schools':schools,'classes':classes,
                                        'form':TeacherResourceForm.TeacherResourceForm()})

@login_required
@switchlanguage
def resource_units(request):
    return render(request, 
                  'portalteacher/resource_units.html', 
                  {'resource_units':resource_units,
                   'classid': request.GET.get('classid'),
                   'section': request.GET.get('section')
                  })

@login_required
@switchlanguage
def resourcelist(request):
    return render(request, 'portalteacher/resourcelist.html', 
                    {'resourcelist':resourcelist })

@login_required
@switchlanguage
def extraslist(request):
    #studentresourceunits_body = models.Chapterinfo.objects.all()
    return render(request, 
                  'portalteacher/extraslist.html', 
                  {'extraslist':extraslist,
                   'classid': request.GET.get('classid'),
                   'section': request.GET.get('section')    
                  })


@login_required
@switchlanguage
def rubrics(request):
    return render(request, 'portalteacher/rubrics.html')

@login_required
@switchlanguage
def statistics(request):
    folders = [{
        "id": "1",
        "name" :_("Login statistics"),
        "href" :"statisticsstudentslist"
        },{
        "id": "2",
        "name" :_("Assignment statistics"),
        "href" :"statisticsstudentslist"
        },{
        "id": "3",
        "name" :_("Exercises Statistics"),
        "href" :"statisticsstudentslist"
        }]
    return render(request, 'portalteacher/statistics.html', 
                  {"folders":folders,'statistics':statistics})

@login_required
@switchlanguage
def statisticsstudentslist(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/statisticsstudentslist.html', 
                                        {'schools':schools, 'classes':classes, 
                                        "form" : StudentForm.StudentForm()} )

@login_required
@switchlanguage
def rubric_edit(request):
    return render(request, 'portalteacher/rubric_edit.html' ,{
                            "form" : RubricsForm.RubricsForm() })

@login_required
@switchlanguage
def rubric_view(request):
    rubricid =  request.GET.get("rubricid")
    return render(request, 'portalteacher/rubric_view.html' ,{
                            "form" : RubricsForm.RubricsForm() })

@login_required
@switchlanguage                
def viewassignresource(request):
    return render(request, 'portalteacher/viewassignresource.html')
    
@login_required
@switchlanguage
def viewassignmentanswer(request):
    return render(request, 'portalteacher/viewassignmentanswer.html') 

@login_required
@switchlanguage
def stickynotes(request):
    return render(request, 'portalteacher/stickynotes.html', 
                                        {'form':StickyForm.StickyForm(),
                                         'Cform':StickyCommentForm.StickyCommentForm()
                                         })                     
@login_required
@switchlanguage
def billboard(request):
    return render(request, 'portalteacher/billboard.html')

@login_required
@switchlanguage
def activitystatistics(request):
    return render(request, 'portalteacher/activitystatistics.html')
    
@login_required
@switchlanguage
def topics(request):
    return render(request, 'portalteacher/forum.html',{"form" : ForumForm.ForumForm()})
    
@login_required
@switchlanguage
def thread(request):
    topics = models.Topicinfo.objects.all()
    return render(request, 'portalteacher/thread.html', 
                                        {'topics':topics,
                                        "form" : ThreadForm.ThreadForm()})

@login_required
@switchlanguage
def addwrittenwork(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/addwrittenwork.html',{'schools':schools,'classes':classes})

@login_required
@switchlanguage
def threadview(request):
    return render(request, 'portalteacher/threadview.html')
    
   
@login_required
@switchlanguage
def bulletinboardlist(request):
    return render(request, 'portalteacher/bulletinboardlist.html', {"form" : AnnouncementForm.AnnouncementForm()})

@login_required
@switchlanguage
def bulletinboard(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    return render(request, 'portalteacher/bulletinboard.html',
                                        {'schools':schools })
@login_required
@switchlanguage
def studentprofile(request):
    # user = models.Studentinfo.objects.filter(username=request.user.username)[0]
    user=request.GET.get('studentid');
    folders = [{
        "id"   :"1",
        "name" :_("Assignments"),
        "href" :"studentassignedresourcelist"
        },{
        "id"   :"2",
        "name" :_("Written Work"),
        "href" :"viewstudentwrittenworks?studentid=%s" % request.GET.get('studentid') 
        }]
    return render(request, 'portalteacher/studentprofile.html', 
                  {"folders":folders})

@login_required
@switchlanguage
def studentassignedresourcelist(request):
    return render(request, 'portalteacher/studentassignedresourcelist.html')

@login_required
@switchlanguage
def viewstudentwrittenworks(request):
    return render(request, 'portalteacher/viewstudentwrittenworks.html')

@login_required
@switchlanguage
def mindmaplist(request):
    return render(request, "portalteacher/mindmaplist.html", {})

@login_required
@switchlanguage
def mindmapedit(request):
    return render(request, 'portalteacher/mindmap.html', {})
    

@login_required
@switchlanguage
def stickynoteslist(request):
    return render(request, 'portalteacher/stickynoteslist.html',{'form':StickyinfoForm.StickyinfoForm()})                     

@login_required
@switchlanguage
def forum(request):
    return render(request, 'portalteacher/forum.html', {"form" : ForumForm.ForumForm()})

@login_required
@switchlanguage
def viewtopic(request):
   foruminfo = models.Foruminfo.objects.all()
   return render(request, 'portalteacher/viewtopic.html')

def viewpost(request):
    return render(request, 'portalteacher/viewpost.html')

def newtopic(request):
    return render(request, 'portalteacher/newtopic.html', {"form" : NewtopicForm.NewtopicForm()})

@switchlanguage
def classviewassignmentanswer(request):
    return render(request, 'portalteacher/classviewassignmentanswer.html')

@login_required
@switchlanguage
def viewbulletinboard(request):
    return render(request, 'portalteacher/viewbulletinboard.html')

@switchlanguage
def viewassignwrittenwork(request):
    return render(request, 'portalteacher/viewassignwrittenwork.html')

@login_required
@switchlanguage
def viewteacherresource(request):
    return render(request, 'portalteacher/viewteacherresource.html')

@login_required
@switchlanguage
def viewassignwrittenworkanswer(request):
    return render(request, 'portalteacher/viewassignwrittenworkanswer.html')

@login_required
@switchlanguage
def myresourcelist(request):
    return render(request, 'portalteacher/myresourcelist.html', 
                                        {"form" : MyresourcelistForm.MyresourcelistForm()})

@login_required
@switchlanguage
def viewmyresourcelist(request):
    return render(request, 'portalteacher/viewmyresourcelistwork.html')

@login_required
@switchlanguage
def classviewassignwrittenworkanswer(request):
    return render(request, 'portalteacher/classviewassignwrittenworkanswer.html')

@login_required
@switchlanguage
def viewresourcelist(request):
    return render(request, 'portalteacher/viewresourcelist.html')

@login_required
@switchlanguage
def studentmindmaplist(request):
    return render(request, 'portalteacher/studentmindmaplist.html')

@login_required
@switchlanguage
def assignmindmap(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/assignmindmap.html',{'schools':schools,'classes':classes})
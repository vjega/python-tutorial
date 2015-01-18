# -*- coding: utf-8 -*-
from django.utils.translation import (ugettext as _, activate)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from portaladmin import models
from django.utils.safestring import mark_safe

from portaladmin.forms import (AdminForm,
			       TeacherResourceForm,
                   TeacherForm,
                   StudentForm,
                   SchoolListForm,
                   StudentresourceListForm,
                   ClassListForm,
                   CalendarForm,
                   StickyForm,
                   StickyCommentForm,
                   AnnouncementForm,
                   BillviewassignmentanswerForm,
                   BillcomprehensionanswerratingForm,
                   StickyinfoForm,
                   MyresourcelistForm
                    )
from ajaxuploader.views import AjaxFileUploader
#from ajaxuploader.backends.easythumbnails import EasyThumbnailUploadBackend

def switchlanguage(f):
    def inner(req):
        print req.session.get('django_language')
        activate(req.session.get('django_language','ta'))
        return f(req)
    return inner

def checkaccess(utype):
    def outer(f):
        def inner(*arg, **kwarg):
            return f(*arg, **kwarg)
        return inner
    return outer




admin_img_uploader = AjaxFileUploader(UPLOAD_DIR='static/admins', 
                                      DIMENSIONS=(250, 250))
teacher_img_uploader = AjaxFileUploader(UPLOAD_DIR='static/teachers', 
                                      DIMENSIONS=(250, 250))

student_img_uploader = AjaxFileUploader(UPLOAD_DIR='static/students', 
                                      DIMENSIONS=(250, 250))

student_studentres_uploader = AjaxFileUploader(UPLOAD_DIR='static/studentres')

student_teacherres_uploader = AjaxFileUploader(UPLOAD_DIR='static/teacherres')

bulletinboard_uploader = AjaxFileUploader(UPLOAD_DIR='static/bulletinboard')

writtenwork_uploader = AjaxFileUploader(UPLOAD_DIR='static/writtenwork')

def layoutdemo(request):
    return render(request, 'portaladmin/layoutdemo.html')

@login_required
@switchlanguage
def home(request):
    folders = [{
        "color": u"primary",
        "icon" : u"flaticon-school43",
        "link" : u"schoollist",
        "caption": _("Schools"),
        "stat": 25
        }, {
        "color": u"green",
        "icon" : u"flaticon-books24",
        "link" : u"teacherresourcelist",
        "caption": u"{0} {1}".format(_("Teachers"),_("Resources")),
        "stat": 64
        }, {
        "color": u"red",
        "icon" : u"flaticon-education32",
        "link" : u"studentresourcetype",
        "caption": u"{0} {1}".format(_("Student"), _("Resources")),
        "stat": 125
        }]

    recent_acitivity_head = [_("Sl No."),
                             _("Assignments"),
                             _("Date")]
    admin_folders = models.AdminFolders.folders(request)
    announcement_body = models.Bulletinboardinfo.announcement(request)
    recent_activity_body = models.Activitylog.recentactivities()
    recent_activities = {'head':recent_acitivity_head,
                         'body':recent_activity_body}
    announcement = {'body':announcement_body}
    return  render(request, 'portaladmin/index.html', {"folders":folders,
                                           "admin_folders":admin_folders,
                                           "recent_activities":recent_activities,
                                           "announcement":announcement
                                           })

@login_required
@switchlanguage
def adminlist(request):
    return render(request, 'portaladmin/adminlist.html', 
                                        {"adminform" : AdminForm.AdminForm()})

@login_required
@switchlanguage
def teacherslist(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    return render(request, 'portaladmin/teacherslist.html', 
                                        {'schools':schools,
                                        "form" : TeacherForm.TeacherForm()})

@login_required
@switchlanguage
def studentslist(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    classes = models.Classinfo.objects.all()
    return render(request, 'portaladmin/studentslist.html', 
                                      {'schools':schools, 'classes':classes, 
                                        "form" : StudentForm.StudentForm()})           

@login_required
@switchlanguage
def schoollist(request):
    return render(request, 'portaladmin/schoollist.html',{
                                        "form" : SchoolListForm.SchoolListForm()})


@login_required
@switchlanguage
def teacherresourcelist(request):
    return render(request, 'portaladmin/teacherresourcelist.html', {
                                        'form':TeacherResourceForm.TeacherResourceForm()})

@login_required
@switchlanguage
def viewteacherresource(request):
    viewteacherresource_head = [('Sl No.')]
    viewteacherresource = {'head':viewteacherresource_head }
    return render(request, 'portaladmin/viewteacherresource.html')

@login_required
@switchlanguage
def studentresourcetype(request):
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
    return render(request, 'portaladmin/studentresource_type.html', 
                  {"folders":folders,'studentresourcetype':studentresourcetype})

@login_required
@switchlanguage
def resourcetype(request):
    folders = [{
        "id": "1",
        "categoryid": "0",
        "name" :_(u"Reading"),
        "href" :u"chapterlist"
        },{
        "id": "2",
        "categoryid": "1",
        "name" :_(u"Image dialog"),
        "href" :u"chapterlist"
        },{
        "id": "3",
        "categoryid": "2",
        "name" :_(u"Writing board"),
        "href" :u"chapterlist"
        }]
    classid = request.GET.get('classid')
    section = request.GET.get('section')
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portaladmin/resource_type.html', 
                  {"folders":folders,
                   "resourcetype":resourcetype,
                   "classid":classid,
                   "section":section})

@login_required
@switchlanguage
def extralist(request):
    folders = [{
        "id": "1",
        "name" :u"writing",
        "href" :""
        },{
        "id": "2",
        "name" :u"Multimedia",
        "href" :""
        },{
        "id": "3",
        "name" :u"Lyrics",
        "href" :""
        },{
        "id": "4",
        "name" :u"Olippatakkatci",
        "href" :""
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'resource_type.html', 
                  {"folders":folders,'resourcetype':resourcetype})


@login_required
@switchlanguage
def chapterlist(request):
    chapterlist_body = models.Chapterinfo.objects.all()
    return render(request, 
                  'portaladmin/chapterlist.html', 
                  {'chapterlist':chapterlist,
                   'classid': request.GET.get('classid'),
                   'section': request.GET.get('section')
                  })

@login_required
@switchlanguage
def viewstudentresourcelist(request):
    viewstudentresourcelist_body = models.Chapterinfo.objects.all()
    return render(request, 
                  'portaladmin/viewstudentresourcelist.html', 
                  {'viewstudentresourcelist':viewstudentresourcelist,
                   'classid': request.GET.get('classid'),
                   'section': request.GET.get('section')
                  })

@login_required
def viewstudentwrittenworks(request):
    viewstudentwrittenworks_head = [('Sl No.'),
                         _('Name'),
                         _('Short Name'),
                         _('Edit'),
                         _('Delete')]
    viewstudentwrittenworks_body = models.Schoolinfo.objects.all().order_by('schoolname')
    viewstudentwrittenworks = {'head':viewstudentwrittenworks_head, 'body':viewstudentwrittenworks_body}
    return render(request, 'portaladmin/viewstudentwrittenworks.html')


@login_required
@switchlanguage
def classlist(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    return render(request, 'portaladmin/classlist.html', 
                  {'schools':schools, "form" : ClassListForm.ClassListForm()}
                  )

@login_required
@switchlanguage
def statistics(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    return render(request, 'portaladmin/statistics.html', {'schools':schools})
   

@login_required
@switchlanguage
def classroom(request):
    studentslist_head = [_('Sl No.'),
                         _('Photo'),
                         _('Name'),
                         _('User Name'),
                         _('Email Id'),
                         _('Edit'),
                         _('Delete')]
    studentslist_body = [{
                             'no':1, 
                             'img':'http://placehold.it/80x80', 
                             'loginname':'johdoe',
                             'name' :'John Doe',
                             'email':'johndoe@acme.com'
                         },{
                             'no':2, 
                             'img':'http://placehold.it/80x80', 
                             'loginname':'johdoe',
                             'name' :'John Doe',
                             'email':'johndoe@acme.com'
                         },{
                             'no':3, 
                             'img':'http://placehold.it/80x80', 
                             'loginname':'johdoe',
                             'name' :'John Doe',
                             'email':'johndoe@acme.com'
                         },{
                             'no':4, 
                             'img':'http://placehold.it/80x80', 
                             'loginname':'johdoe',
                             'name' :'John Doe',
                             'email':'johndoe@acme.com'
                         }]
    studentslist = {'head':studentslist_head, 'body':studentslist_body}
    return render(request, 'portaladmin/classroom.html', {'studentslist':studentslist})

@login_required
@switchlanguage
def billboard(request):
    studentslist_head = [_('Sl No.'),
                         _('Photo'),
                         _('Name'),
                         _('User Name'),
                         _('Email Id'),
                         _('Edit'),
                         _('Delete')]
    studentslist_body = [{
                             'no':1, 
                             'img':'http://placehold.it/80x80', 
                             'loginname':'johdoe',
                             'name' :'John Doe',
                             'email':'johndoe@acme.com'
                         },{
                             'no':2, 
                             'img':'http://placehold.it/80x80', 
                             'loginname':'johdoe',
                             'name' :'John Doe',
                             'email':'johndoe@acme.com'
                         },{
                             'no':3, 
                             'img':'http://placehold.it/80x80', 
                             'loginname':'johdoe',
                             'name' :'John Doe',
                             'email':'johndoe@acme.com'
                         },{
                             'no':4, 
                             'img':'http://placehold.it/80x80', 
                             'loginname':'johdoe',
                             'name' :'John Doe',
                             'email':'johndoe@acme.com'
                         }]
    studentslist = {'head':studentslist_head, 'body':studentslist_body}
    return render(request, 'portaladmin/billboard.html')

@login_required
@switchlanguage
def mindmapedit(request, id):
    return render(request, 'portaladmin/mindmap.html', {})
    
@login_required
@switchlanguage
def stickynotes(request):
    return render(request, 'portaladmin/stickynotes.html', 
                                        {'form':StickyForm.StickyForm(),
                                         'Cform':StickyCommentForm.StickyCommentForm()
                                         })
    
@login_required
@switchlanguage
def calendar(request):
    return render(request, 'portaladmin/calendar.html', {"calendarform" : CalendarForm.CalendarForm()})
    
@login_required
@switchlanguage
def recorder(request):
    return render(request, 'portaladmin/recorder.html', {})

@login_required
@switchlanguage
def studentresourcelist(request):
    return render(request, 'portaladmin/studentresourcelist.html', 
                    {'studentslist':studentslist,
                     "form" : StudentresourceListForm.StudentresourceListForm()})

@login_required
@switchlanguage
def subjectlist(request):
    return HttpResponse("Not implemented", 404)

@login_required
@switchlanguage
def studentprofile(request):
    folders = [{
        "id"   : "1",
        "name" :u"Assessment",
        "href" :u"studentassignedresourcelist"
        },{
        "id"   : "2",
        "name" :u"Writing job",
        "href" :u"viewstudentwrittenworks?studentid=%s" % request.GET.get('studentid') 
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portaladmin/studentprofile.html', 
                  {"folders":folders})

@login_required
@switchlanguage
def studentassignedresourcelist(request):
    '''assigned_head = [_('Sl No.'),
                         _('Title'),
                         _('Type'),
                         _('Date'),
                         _('Note')]
    studentslist = {'assigned_head':assigned_head}'''
    return render(request, 'portaladmin/studentassignedresourcelist.html')

@login_required
@switchlanguage
def viewstudentwork(request):
    return render(request, 'portaladmin/viewstudentwork.html')

@login_required
@switchlanguage
def mindmaplist(request):
    return render(request, "portaladmin/mindmaplist.html", {})

@login_required
@switchlanguage
def mindmapedit(request):
    return render(request, 'portaladmin/mindmap.html', {})

@login_required
@switchlanguage
def bulletinboardlist(request):
    return render(request, 'portaladmin/bulletinboardlist.html', {"form" : AnnouncementForm.AnnouncementForm()})

@login_required
@switchlanguage
def bulletinboard(request):
    schools = models.Schoolinfo.objects.all().order_by('schoolname')
    return render(request, 'portaladmin/bulletinboard.html',
                                        {'schools':schools })

@login_required
@switchlanguage
def billboard(request):
    return render(request, 'portaladmin/billboard.html')

@login_required
@switchlanguage
def billviewassignmentanswer(request):
    return render(request, 'portaladmin/billviewassignmentanswer.html',{"form":BillviewassignmentanswerForm.BillviewassignmentanswerForm()})

@login_required
@switchlanguage
def billviewwrittenworkanswer(request):
    return render(request, 'portaladmin/billviewwrittenworkanswer.html')

@login_required
@switchlanguage
def billfillinganswerrating(request):
    return render(request, 'portaladmin/billfillinganswerrating.html')

@login_required
@switchlanguage
def billchooseanswerrating(request):
    return render(request, 'portaladmin/billchooseanswerrating.html')

@login_required
@switchlanguage
def billcomprehensionanswerrating(request):
    return render(request, 'portaladmin/billcomprehensionanswerrating.html',
                        {"form":BillcomprehensionanswerratingForm.BillcomprehensionanswerratingForm})

@login_required
@switchlanguage
def billopenendedanswerrating(request):
    return render(request, 'portaladmin/billopenendedanswerrating.html')

@login_required
@switchlanguage
def stickynoteslist(request):
    return render(request, 'portaladmin/stickynoteslist.html',{'form':StickyinfoForm.StickyinfoForm()})
                        
@login_required
@switchlanguage
def topics(request):
    return render(request, 'portaladmin/topics.html',{"form" : TopicsForm.TopicsForm()})

@login_required
@switchlanguage
def myresourcelist(request):
    return render(request, 'portaladmin/myresourcelist.html', 
                                        {"form" : MyresourcelistForm.MyresourcelistForm()})

@login_required
@switchlanguage
def viewbulletinboard(request):
    return render(request, 'portaladmin/viewbulletinboard.html')

@login_required
@switchlanguage
def resources(request):
    folders = [{
        "id": "2",
        "categoryid": "1",
        "name" :_("Lesson Plans"),
        "href" :"teacherresourcelist"
        },{
        "id": "3",
        "categoryid": "2",
        "name" :_("Schools resources"),
        "href" :"teacherresourcelist"
        }]

    return render(request, 'portaladmin/resources.html', 
                  {"folders":folders,'resources':resources})

@login_required
@switchlanguage
def classviewassignmentanswer(request):
    return render(request, 'portaladmin/classviewassignmentanswer.html')
    
@login_required
@switchlanguage
def viewmyresourcelist(request):
    return render(request, 'portaladmin/viewmyresourcelistwork.html')

@login_required
@switchlanguage   
def classviewassignwrittenworkanswer(request):
    return render(request, 'portaladmin/classviewassignwrittenworkanswer.html')    

@login_required
@switchlanguage
def rubrics(request):
    return render(request, 'portaladmin/rubrics.html')
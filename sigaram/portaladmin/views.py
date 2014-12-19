# -*- coding: utf-8 -*-
from django.utils.translation import (ugettext as _, activate)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from portaladmin import models
from portaladmin.forms import (AdminForm,
			       TeacherResourceForm,
                   TeacherForm,
                   StudentForm,
                   SchoolListForm,
                   StudentresourceListForm,
                   ClassListForm,
                   CalendarForm,)
from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.easythumbnails import EasyThumbnailUploadBackend

def switchlanguage(f):
    def inner(req):
        activate(req.session.get('django_language','ta'))
        return f(req)
    return inner


admin_img_uploader = AjaxFileUploader(UPLOAD_DIR='static/admins', 
                                      #backend=EasyThumbnailUploadBackend, 
                                      DIMENSIONS=(250, 250))
@login_required
def home(request):
    folders = [{
        "color": u"primary",
        "icon" : u"university",
        "link" : u"schoollist",
        "caption": _("Schools"),
        "stat": 25
        }, {
        "color": u"green",
        "icon" : u"book",
        "link" : u"teacherresourcelist",
        "caption": u"{0} {1}".format(_("Teachers"),_("Resources")),
        "stat": 64
        }, {
        "color": u"yellow",
        "icon" : u"book",
        "link" : u"studentresourcetype",
        "caption": u"{0} {1}".format(_("Student"), _("Resources")),
        "stat": 125
        }]

    recent_acitivity_head = [_("Sl No."),_("Assignments"),_("Date")]
    admin_folders = models.AdminFolders.objects.all()
    recent_activity_body = models.Activitylog.recentactivities()
    recent_activities = {'head':recent_acitivity_head,
                         'body':recent_activity_body}
    return  render(request, 'portaladmin/index.html', {"folders":folders,
                                           "admin_folders":admin_folders,
                                           "recent_activities":recent_activities
                                           })

@login_required
def adminlist(request):
    return render(request, 'portaladmin/adminlist.html', 
                                        {"adminform" : AdminForm.AdminForm()})

@login_required
def teacherslist(request):
    schools = models.Schoolinfo.objects.all()
    return render(request, 'portaladmin/teacherslist.html', 
                                        {'schools':schools,
                                        "form" : TeacherForm.TeacherForm()})

@login_required
#@switchlanguage
def studentslist(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portaladmin/studentslist.html', 
                                      {'schools':schools, 'classes':classes, 
                                        "form" : StudentForm.StudentForm()})           

@login_required
def schoollist(request):
    return render(request, 'portaladmin/schoollist.html',{
                                        "form" : SchoolListForm.SchoolListForm()})


@login_required
def teacherresourcelist(request):
    return render(request, 'portaladmin/teacherresourcelist.html', {
                                        'form':TeacherResourceForm.TeacherResourceForm()})

@login_required
def viewteacherresource(request):
    viewteacherresource_head = [('Sl No.')]
    viewteacherresource = {'head':viewteacherresource_head }
    return render(request, 'portaladmin/viewteacherresource.html')

@login_required
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
def resourcetype(request):
    folders = [{
        "id": "1",
        "categoryid": "0",
        "name" :"வாசிப்பு",
        "href" :"chapterlist"
        },{
        "id": "2",
        "categoryid": "1",
        "name" :"பட உரையாடல்",
        "href" :"chapterlist"
        },{
        "id": "3",
        "categoryid": "2",
        "name" :"எழுத்து பலகை",
        "href" :"chapterlist"
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
def extralist(request):
    folders = [{
        "id": "1",
        "name" :"எழுத்து",
        "href" :""
        },{
        "id": "2",
        "name" :"பல்லூடகம்",
        "href" :""
        },{
        "id": "3",
        "name" :"பாடல்",
        "href" :""
        },{
        "id": "4",
        "name" :"ஒளிப்படக்காட்சி",
        "href" :""
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'resource_type.html', 
                  {"folders":folders,'resourcetype':resourcetype})


@login_required
def chapterlist(request):
    chapterlist_body = models.Chapterinfo.objects.all()
    return render(request, 
                  'portaladmin/chapterlist.html', 
                  {'chapterlist':chapterlist,
                   'classid': request.GET.get('classid'),
                   'section': request.GET.get('section')
                  })

@login_required
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
    viewstudentwrittenworks_body = models.Schoolinfo.objects.all()
    viewstudentwrittenworks = {'head':viewstudentwrittenworks_head, 'body':viewstudentwrittenworks_body}
    return render(request, 'portaladmin/viewstudentwrittenworks.html')


@login_required
def classlist(request):
    schools = models.Schoolinfo.objects.all()
    return render(request, 'portaladmin/classlist.html', 
                  {'schools':schools, "form" : ClassListForm.ClassListForm()}
                  )

@login_required
def statistics(request):
    schools = models.Schoolinfo.objects.all()
    return render(request, 'portaladmin/statistics.html', {'schools':schools})
   

@login_required
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
    return render(request, 'portaladmin/studentslist.html', {'studentslist':studentslist})

@login_required
def mindmapedit(request, id):
    return render(request, 'portaladmin/mindmap.html', {})
    
@login_required
def sticky_notes(request):
    return render(request, 'portaladmin/sticky_notes.html', {})
    
@login_required
def calendar(request):
    return render(request, 'portaladmin/calendar.html', {"calendarform" : CalendarForm.CalendarForm()})
    
@login_required
def recorder(request):
    return render(request, 'portaladmin/recorder.html', {})

@login_required
def studentresourcelist(request):
    return render(request, 'portaladmin/studentresourcelist.html', 
                    {'studentslist':studentslist,
                     "form" : StudentresourceListForm.StudentresourceListForm()})

@login_required
def subjectlist(request):
    return HttpResponse("Not implemented", 404)

@login_required
def studentprofile(request):
    folders = [{
        "id"   : "1",
        "name" :"Deliverables",
        "href" :"studentassignedresourcelist"
        },{
        "id"   : "2",
        "name" :"Writing job",
        "href" :"viewstudentwrittenworks?studentid=%s" % request.GET.get('studentid') 
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portaladmin/studentprofile.html', 
                  {"folders":folders})

@login_required
def studentassignedresourcelist(request):
    '''assigned_head = [_('Sl No.'),
                         _('Title'),
                         _('Type'),
                         _('Date'),
                         _('Note')]
    studentslist = {'assigned_head':assigned_head}'''
    return render(request, 'portaladmin/studentassignedresourcelist.html')

@login_required
def viewstudentwork(request):
    return render(request, 'portaladmin/viewstudentwork.html')

def mindmaplist(request):
    return render(request, "portaladmin/mindmaplist.html", {})

@login_required
def mindmapedit(request):
    return render(request, 'portaladmin/mindmap.html', {})

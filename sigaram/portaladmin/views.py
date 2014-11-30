# -*- coding: utf-8 -*-
from django.utils.translation import (ugettext as _, activate)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from portaladmin import models
from portaladmin.forms import (AdminForm,
			       TeacherResourceForm,
                   TeacherListForm)	

def switchlanguage(f):
    def inner(req):
        activate(req.session.get('django_language','ta'))
        return f(req)
    return inner

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
    return render(request, 'portaladmin/adminlist.html', {"adminform" : AdminForm.AdminForm()})

@login_required
def teacherslist(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portaladmin/teacherslist.html', 
                                        {'schools':schools,'classes':classes, 
                                        "form" : TeacherListForm.TeacherListForm()})

@login_required
#@switchlanguage
def studentslist(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portaladmin/studentslist.html', {'schools':schools,
                                                             'classes':classes})

@login_required
def schoollist(request):
    schoollist_head = [('Sl No.'),
                         _('Name'),
                         _('Short Name'),
                         _('Edit'),
                         _('Delete')]
    schoollist_body = models.Schoolinfo.objects.all()
    schoollist = {'head':schoollist_head, 'body':schoollist_body}
    return render(request, 'portaladmin/schoollist.html', {'schoollist':schoollist})

@login_required
def teacherresourcelist(request):
    classes = models.Classinfo.objects.all()
    teacherresourcelist_head = [('Sl No.'),
                         _('Title'),
                         _('Date'),
                         _('Type'),
                         _('Delete')]
    teacherresourcelist_body = models.Teacherresourceinfo.objects.all()
    teacherresourcelist = {'head':teacherresourcelist_head, 
                           'body':teacherresourcelist_body}
    return render(request, 'portaladmin/teacherresourcelist.html', 
                  {'classes':classes, 
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
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portaladmin/studentresource_type.html', 
                  {"folders":folders,'studentresourcetype':studentresourcetype})

@login_required
def resourcetype(request):
    folders = [{
        "id": "1",
        "name" :"வாசிப்பு",
        "href" :"chapterlist"
        },{
        "id": "2",
        "name" :"பட உரையாடல்",
        "href" :"chapterlist"
        },{
        "id": "3",
        "name" :"எழுத்து பலகை",
        "href" :"chapterlist"
        }]

    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portaladmin/resource_type.html', 
                  {"folders":folders,'resourcetype':resourcetype})

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
    classinfo = models.Classinfo.objects.all()
    classlist_head = [_('Sl No.'),
                      _('Class Name'),
                      _('Short Name'),
                      _('Delete')]
    classlist = {'head':classlist_head}
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portaladmin/classlist.html', 
                  {"classinfo":classinfo, 'classlist':classlist, 
                  'schools':schools}
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
def mindmap(request):
    return render(request, 'portaladmin/mindmap.html', {})
    
@login_required
def sticky_notes(request):
    return render(request, 'portaladmin/sticky_notes.html', {})
    
@login_required
def calendar(request):
    return render(request, 'portaladmin/calendar.html', {})
    
@login_required
def recorder(request):
    return render(request, 'portaladmin/recorder.html', {})

@login_required
def studentresourcelist(request):
    studentslist_head = [_('Sl No.'),
                         _('Title'),
                         _('Date'),
                         _('Type'),
                         _('Delete')]
    studentslist_body = models.Studentinfo.getlist() 
    studentslist = {'head':studentslist_head, 'body':studentslist_body}
    return render(request, 'portaladmin/studentresourcelist.html', 
                    {'studentslist':studentslist}
                )

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
        "href" :"viewstudentwrittenworks"
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

# -*- coding: utf-8 -*-
from django.utils.translation import (ugettext as _, activate)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from student import models
from portaladmin import models as pmodels
from ajaxuploader.views import AjaxFileUploader
from student.forms import (StudentWorkForm,
                           StudentNotesForm,
                           StickyForm,
                           StickyCommentForm,
                           TopicsForm,
                           StickyinfoForm)


bulletinboard_uploader = AjaxFileUploader(UPLOAD_DIR='static/bulletinboard')

def switchlanguage(f):
    def inner(req):
        activate(req.session.get('django_language','ta'))
        return f(req)
    return inner

@login_required
@switchlanguage
def home(request):
    folders = [{
        "color": u"primary",
        "icon" : u"file-text-o",
        "link" : u"resourcetype",
        "caption": _("Assignments"),
        "stat": 25
        }, {
        "color": u"green",
        "icon" : u"book",
        "link" : u"workspace",
        "caption": _("My works"),
        "stat": 64
        }, {
        "color": u"yellow",
        "icon" : u"pencil-square-o",
        "link" : u"studentnoteslist",
        "caption": _("Notes"),
        "stat": 125
        },{
        "color": u"red",
        "icon" : u"pencil",
        "link" : u"studentwrittenwork",
        "caption": _("Written Work"),
        "stat": 125
        },
        {
        "color": u"green",
        "icon" : u"desktop",
        "link" : u"studentviewassessments",
        "caption": _("Practicals"),
        "stat": 125
        }]

    recent_acitivity_head = [_("Sl No."),
                             _("Assignments"),
                             _("Date")]
    admin_folders = pmodels.AdminFolders.folders(request)
    recent_activity_body = models.Activitylog.recentactivities()
    recent_activities = {'head':recent_acitivity_head,
                         'body':recent_activity_body}
    announcement = pmodels.Bulletinboardinfo.announcement(request)
    return  render(request, 'portalstudent/index.html', {"folders":folders,
                                           "admin_folders":admin_folders,
                                           "recent_activities":recent_activities,
                                           "announcement":announcement})
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
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalstudent/studentresource_type.html', 
                  {"folders":folders,'studentresourcetype':studentresourcetype})

@login_required
@switchlanguage
def resourcetype(request):
    folders = [{
        "categoryid" : "0",
        "id"         : "1",
        "name"       : _("Reading"),
        "href"       :"assignedresourcelist"
        },{
        "categoryid" : "1",
        "id"         : "2",
        "name"       :_("Image dialog"),
        "href"       :"assignedresourcelist"
        },{
        "categoryid" : "3",
        "id"         : "3",
        "name"       :_("Writing board"),
        "href"       :"assignedresourcelist"
        },{
        "categoryid" : "4",
        "id"         : "4",
        "name"       :_("Comprehension"),
        "href"       :"assignedresourcelist"
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalstudent/resource_type.html', 
                  {"folders":folders,'resourcetype':resourcetype})

@login_required
@switchlanguage
def workspace(request):
    folders = [{
        "id"   : "1",
        "name" :_("Character"),
        "href" :"worklistinfo",
        "worktype":"text"
        },{
        "id"   : "2",
        "name" :_("Photography"),
        "href" :"worklistinfo",
        "worktype":"image"
        },{
        "id"   : "3",
        "name" :_("Lyrics"),
        "href" :"worklistinfo",
        "worktype":"audio"
        },{
        "id"   : "4",
        "name" :_("Video"),
        "href" :"worklistinfo",
        "worktype":"video"
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalstudent/workspace.html', 
                  {"folders":folders,'workspace':workspace})

@login_required
@switchlanguage
def studentslist(request):
    user = models.Studentinfo.objects.filter(username=request.user.username)[0]
    return render(request, 'portalstudent/studentslist.html', {'user':user})


@login_required
@switchlanguage
def assignedresourcelist(request):
    return render(request, 'portalstudent/assignedresourcelist.html')

@login_required
@switchlanguage
def studentprofile(request):
    user = models.Studentinfo.objects.filter(username=request.user.username)[0]
    folders = [{
        "id"   :"1",
        # "caption": _("Assignments"),
        "name" :_("Assignments"),
        "href" :"studentassignedresourcelist"
        },{
        "id"   :"2",
        "name" :_("Written Work"),
        "href" :"viewstudentwrittenworks"
        }]
    return render(request, 'portalstudent/studentprofile.html', 
                  {"folders":folders, "user":user})

@login_required
@switchlanguage
def studentassignedresourcelist(request):
    return render(request, 'portalstudent/studentassignedresourcelist.html')

@login_required
@switchlanguage
def viewstudentresource(request):
    return render(request, 'portalstudent/viewstudentresource.html')

@login_required
@switchlanguage
def viewstudentwrittenworks(request):
    return render(request, 'portalstudent/viewstudentwrittenworks.html')

@login_required
@switchlanguage
def viewstudentwork(request):
    return render(request, 'portalstudent/viewstudentwork.html')

@login_required
@switchlanguage
def worklistinfo(request):
    worktype=request.GET.get('workspacetype')
    if worktype=='text':
        title=_('Text')
    elif worktype=='image':
        title=_('Image')
    elif worktype=='audio':
        title=_('Audio')
    else:
        title=_('Video')
    return render(request, 'portalstudent/worklistinfo.html',
                            {"headtitle":title,
                             "workspacetype":worktype,
                             "form" : StudentWorkForm.StudentWorkForm()})
    
@login_required
@switchlanguage
def studentviewwork(request):
    return render(request, 'portalstudent/studentviewwork.html')

@login_required
@switchlanguage
def studentnoteslist(request):
    return render(request, 'portalstudent/studentnoteslist.html',
                            {"form" : StudentNotesForm.StudentNotesForm()})

@login_required
@switchlanguage
def studentwrittenwork(request):
    return render(request, 'portalstudent/studentwrittenwork.html')

@login_required
@switchlanguage
def studentviewassessments(request):
    return render(request, 'portalstudent/studentviewassessments.html')

@login_required
@switchlanguage
def studentclassroom(request):
    return render(request, 'portalstudent/studentclassroom.html')

@login_required
@switchlanguage
def viewassignresource(request):
    return render(request, 'portalstudent/viewassignresource.html')    

@login_required
@switchlanguage
def viewassignmentanswer(request):
    return render(request, 'portalstudent/viewassignmentanswer.html') 

@switchlanguage
@switchlanguage
def stickynotes(request):
    return render(request, 'portalstudent/stickynotes.html', 
                                        {'form':StickyForm.StickyForm(),
                                         'Cform':StickyCommentForm.StickyCommentForm()
                                         })    
@switchlanguage
def billboard(request):
    return render(request, 'portalstudent/billboard.html')

@switchlanguage
def billviewassignmentanswer(request):
    return render(request, 'portalstudent/billviewassignmentanswer.html')

@switchlanguage
def bulletinboardlist(request):
    return render(request, 'portalstudent/bulletinboardlist.html')

@switchlanguage
def bulletinboardlist(request):
    return render(request, 'portalstudent/bulletinboardlist.html')


@switchlanguage
def studentresourceunits(request):
    return render(request, 'portalstudent/studentresourceunits.html',
                 {'classid': request.GET.get('classid'),
                   'section': request.GET.get('section')    
                  })

@switchlanguage
def studentresourcelist(request):
    return render(request, 'portalstudent/studentresourcelist.html')

@login_required
@switchlanguage
def topics(request):
    return render(request, 'portalstudent/topics.html',{"form" : TopicsForm.TopicsForm()})

@login_required
@switchlanguage
def stickynoteslist(request):
    return render(request, 'portalstudent/stickynoteslist.html',{'form':StickyinfoForm.StickyinfoForm()})

@login_required
@switchlanguage
def viewbulletinboard(request):
    return render(request, 'portalstudent/viewbulletinboard.html')
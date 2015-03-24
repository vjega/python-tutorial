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
        "caption": _("Assignments")
        },
        # {
        # "color": u"green",
        # "icon" : u"book",
        # "link" : u"workspace",
        # "caption": _("My works"),
        # "stat": 64
        # },
        {
        "color": u"yellow",
        "icon" : u"pencil-square-o",
        "link" : u"studentnoteslist",
        "caption": _("Notes")
        },{
        "color": u"green",
        "icon" : u"pencil-square-o",
        "link" : u"studentwrittenwork",
        "caption": _("Written Work")
        },
        {
        "color": u"red",
        "icon" : u"pencil",
        "link" : u"assignedassessmentlist",
        "caption": _("Exercises"),
        },
        {
        "color": u"primary",
        "icon" : u"sitemap",
        "link" : u"studentviewmindmap",
        "caption": _("Mindmap")
        }]


    recent_acitivity_head = [_("Sl No."),
                             _("Assignments"),
                             _("Announcer"),
                             _("Date")]
    admin_folders = pmodels.AdminFolders.folders(request)
    recent_activity_body = pmodels.Activitylog.recentactivities(request)
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
    return render(request, 'portalstudent/studentresource_type.html', 
                  {"folders":folders,'studentresourcetype':studentresourcetype})

@login_required
@switchlanguage
def resourcetype(request):
    folders = [{
        "id": "1",
        "categoryid": "0",
        "name" :_("Reading"),
        "href" :"assignedresourcelist"
        },{
        "id": "2",
        "categoryid": "1",
        "name" :_("Animation"),
        "href" :"assignedresourcelist"
        },{
        "id": "3",
        "categoryid": "2",
        "name" :_("Writing board"),
        "href" :"assignedresourcelist"
        },{
        "id": "3",
        "name" :_("Composition"),
        "href" :"assignedresourcelist"
        }]
    classid = request.GET.get('classid',1)
    section = request.GET.get('section','a')
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalstudent/resource_type.html', 
                  {"folders":folders,
                  "resourcetype":resourcetype,
                  "classid":classid,
                  "section":section}
                  )


@login_required
@switchlanguage
def sturesourcetype(request):
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
        },
        {
        "id": "3",
        "name" :_("Composition"),
        "href" :"studentresourceunits"
        }
        ]
    classid = request.GET.get('classid')
    section = request.GET.get('section')
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalstudent/resource_type.html', 
                  {"folders":folders,
                  "resourcetype":resourcetype,
                  "classid":classid,
                  "section":section}
                  )



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
    folders = [{
        "id"   : "1",
        "name" :_("Assignments"),
        "href" :u"studentassignedresourcelist?studentid=%s" % request.GET.get('studentid')
        },{
        "id"   : "2",
        "name" :_("Written Work"),
        "href" :u"studentassignedwrittenworklist?studentid=%s" % request.GET.get('studentid') 
        },{
        "id"   : "3",
        "name" :_("Exercises"),
        "href" :u"studentassignedassessmentlist?studentid=%s" % request.GET.get('studentid') 
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalstudent/studentprofile.html', 
                  {"folders":folders})

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
def classroom(request):
    return render(request, 'portalstudent/classroom.html')

@login_required
@switchlanguage
def viewassignresource(request):
    return render(request, 'portalstudent/viewassignresource.html')    

@login_required
@switchlanguage
def viewassignmentanswer(request):
    return render(request, 'portalstudent/viewassignmentanswer.html') 

@login_required
@switchlanguage
def stickynotes(request):
    return render(request, 'portalstudent/stickynotes.html', 
                                        {'form':StickyForm.StickyForm(),
                                         'Cform':StickyCommentForm.StickyCommentForm()
                                         })    
@login_required
@switchlanguage
def billboard(request):
    return render(request, 'portalstudent/billboard.html')

@login_required
@switchlanguage
def billviewassignmentanswer(request):
    return render(request, 'portalstudent/billviewassignmentanswer.html')

@login_required
@switchlanguage
def bulletinboardlist(request):
    return render(request, 'portalstudent/bulletinboardlist.html')

@login_required
@switchlanguage
def bulletinboardlist(request):
    return render(request, 'portalstudent/bulletinboardlist.html')


@login_required
@switchlanguage
def studentresourceunits(request):
    return render(request, 'portalstudent/studentresourceunits.html',
                 {'classid': request.GET.get('classid'),
                   'section': request.GET.get('section')    
                  })

@login_required
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

@login_required
@switchlanguage
def viewassignwrittenwork(request):
    return render(request, 'portalstudent/viewassignwrittenwork.html')

@login_required
@switchlanguage
def viewassignwrittenworkanswer(request):
    return render(request, 'portalstudent/viewassignwrittenworkanswer.html')

@login_required
@switchlanguage
def classviewassignmentanswer(request):
    return render(request, 'portalstudent/classviewassignmentanswer.html') 

@login_required
@switchlanguage
def classviewassignwrittenworkanswer(request):
    return render(request, 'portalstudent/classviewassignwrittenworkanswer.html')

@login_required
@switchlanguage
def studentviewmindmap(request):
    return render(request, 'portalstudent/studentviewmindmap.html')

@login_required
@switchlanguage
def viewassignmindmap(request):
    return render(request, 'portalstudent/viewassignmindmap.html')

@login_required
@switchlanguage
def viewassignmindmapanswer(request):
    return render(request, 'portalstudent/viewassignmindmapanswer.html')    

@login_required
@switchlanguage
def viewtopic(request):
   return render(request, 'portalstudent/viewtopic.html')

@login_required
@switchlanguage
def newtopic(request):
    return render(request, 'portalstudent/newtopic.html')

@login_required
@switchlanguage
def viewpost(request):
    return render(request, 'portalstudent/viewpost.html')

@login_required
@switchlanguage
def billboardviewassignwrittenworkanswer(request):
    return render(request, 'portalstudent/billboardviewassignwrittenworkanswer.html')

@login_required
@switchlanguage
def billboardviewassignmentanswer(request):
    return render(request, 'portalstudent/billboardviewassignresourceanswer.html') 

@login_required
@switchlanguage
def assignedassessmentlist(request):
    return render(request, 'portalstudent/assignedassessmentlist.html')

@login_required
@switchlanguage
def viewassignassessment(request):
    return render(request, 'portalstudent/viewassignassessment.html')

@login_required
@switchlanguage
def viewassessmentanswer(request):
    return render(request, 'portalstudent/viewassessmentanswer.html')

@login_required
@switchlanguage
def viewassignopenended(request):
    return render(request, 'portalstudent/viewassignopenended.html')

@login_required
@switchlanguage
def viewopenendedanswer(request):
    return render(request, 'portalstudent/viewopenendedanswer.html')

@login_required
@switchlanguage
def studentassignedwrittenworklist(request):
    '''assigned_head = [_('Sl No.'),
                         _('Title'),
                         _('Type'),
                         _('Date'),
                         _('Note')]
    studentslist = {'assigned_head':assigned_head}'''
    return render(request, 'portalstudent/studentassignedwrittenworklist.html')

@login_required
@switchlanguage
def studentassignedassessmentlist(request):
    '''assigned_head = [_('Sl No.'),
                         _('Title'),
                         _('Type'),
                         _('Date'),
                         _('Note')]
    studentslist = {'assigned_head':assigned_head}'''
    return render(request, 'portalstudent/studentassignedassessmentlist.html')

@login_required
@switchlanguage
def viewstudentwrittenwork(request):
    return render(request, 'portalstudent/viewstudentwrittenwork.html')

@login_required
@switchlanguage
def viewstudentassessmentwork(request):
    return render(request, 'portalstudent/viewstudentassessmentwork.html')
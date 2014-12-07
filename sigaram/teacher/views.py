# -*- coding: utf-8 -*-
from django.utils.translation import (ugettext as _, activate)
from django.shortcuts import render
from teacher import models
from teacher.forms import (ViewworkspaceForm)   

def switchlanguage(f):
    def inner(req):
        activate(req.session.get('django_language','ta'))
        return f(req)
    return inner

@switchlanguage
def home(request):
    folders = [{
        "color": u"primary",
        "icon" : u"file-text-o",
        "link" : u"assignedresourcelist",
        "caption": _("Dedication"),
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
        "link" : u"writtenwork",
        "caption":_("Written Work"),
        "stat": 125
        },{
        "color": u"red",
        "icon" : u"pencil",
        "link" : u"viewassessments",
        "caption": _("Exercises"),
        "stat": 125
        }]

    recent_acitivity_head = [_("Sl No."),_("Assignments"),_("Date")]
    admin_folders = models.AdminFolders.objects.all()
    recent_activity_body = models.Activitylog.recentactivities()
    recent_activities = {'head':recent_acitivity_head,
                         'body':recent_activity_body}
    return  render(request, 'portalteacher/index.html', {"folders":folders,
                                           "admin_folders":admin_folders,
                                           "recent_activities":recent_activities
                                           })

@switchlanguage
def assignedresourcelist(request):
    return render(request, 'portalteacher/assignedresourcelist.html')

@switchlanguage
def workspace(request):
    folders = [{
        "id": "1",
        "name" :_("Writing"),
        "href" :"viewworkspacelist",
        "type" : "Text"
        },{
        "id": "2",
        "name" :_("Image"),
        "href" :"viewworkspacelist",
        "type" : "Image"
        },{
        "id": "3",
        "name" :_("Audio"),
        "href" :"viewworkspacelist",
        "type" :"Audio"
        },{
        "id": "4",
        "name" :_("Video"),
        "href" :"viewworkspacelist",
        "type" : "Video"
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalteacher/workspace.html', 
                  {"folders":folders,'workspace':workspace})

@switchlanguage
def viewworkspacelist(request):
   # print request.GET.get('type')
    return render(request, 'portalteacher/viewworkspacelist.html', {'opt':request.GET.get('type'),
                                                 "form" : ViewworkspaceForm.ViewworkspaceForm()})

@switchlanguage
def writtenwork(request):
    return render(request, 'portalteacher/writtenwork.html',{
                                        "form" : WrittenworkForm.WrittenworkForm()})

@switchlanguage
def viewassessments(request):
    return render(request, 'portalteacher/viewassessments.html')

@switchlanguage
def adminlist(request):
    return render(request, 'portalteacher/adminlist.html')

@switchlanguage
def teacherslist(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/teacherslist.html', 
                                        {'schools':schools,'classes':classes})

@switchlanguage
def studentslist(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/studentslist.html', {'schools':schools,
                                                             'classes':classes})

@switchlanguage
def classroom(request):
    return render(request, 'portalteacher/classroom.html')

@switchlanguage
def myprofile(request):
    return render(request, 'portalteacher/myprofile.html')

@switchlanguage
def allschoolresourcelist(request):
    schools = models.Schoolinfo.objects.all()
    #teacherresourceinfo = models.Teacherresourceinfo.objects.all()
    return render(request, 'portalteacher/allschoolresourcelist.html', {'schools':schools,
                                                                        'teacherresourceinfo':teacherresourceinfo})

@switchlanguage
def students(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/students.html', {'schools':schools,
                                                             'classes':classes})


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
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalteacher/studentresources.html', 
                  {"folders":folders,'studentresources':studentresources})

@switchlanguage
def studentresourcetype(request):
    folders = [{
        "id": "1",
        "categoryid": "0",
        "name" :_("Readings"),
        "href" :"studentresourceunits"
        },{
        "id": "2",
        "categoryid": "1",
        "name" :_("Animation"),
        "href" :"studentresourceunits"
        },{
        "id": "3",
        "categoryid": "2",
        "name" :_("Writing Board"),
        "href" :"studentresourceunits"
        }]

    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalteacher/studentresourcetype.html', 
                  {"folders":folders,'studentresourcetype':studentresourcetype})

@switchlanguage
def studentresourceunits(request):
    #studentresourceunits_body = models.Chapterinfo.objects.all()
    return render(request, 
                  'portalteacher/studentresourceunits.html', 
                  {'studentresourceunits':studentresourceunits,
                   'classid': request.GET.get('classid'),
                   'section': request.GET.get('section')    
                  })

@switchlanguage
def studentresourcelist(request):
    return render(request, 'portalteacher/studentresourcelist.html', 
                    {'studentresourcelist':studentresourcelist}) 

@switchlanguage
def assignchapter(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/assignchapter.html', 
                    {'assignchapter':assignchapter,'schools':schools,
                                             'classes':classes   }) 

@switchlanguage
def resources(request):
    folders = [{
        "id": "1",
        "categoryid": "0",
        "name" :_("Hearing observation"),
        "href" :"resource_type"
        },{
        "id": "2",
        "categoryid": "1",
        "name" :_("Sing notes"),
        "href" :"resource_type"
        },{
        "id": "3",
        "categoryid": "2",
        "name" :_("All schools"),
        "href" :"allschoolresourcelist"
        }]

    return render(request, 'portalteacher/resources.html', 
                  {"folders":folders,'resources':resources})

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
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalteacher/resource_type.html', 
                  {"folders":folders,'resource_type':resource_type})


@switchlanguage
def allschoolresourcelist(request):
    schools = models.Schoolinfo.objects.all()
    classes = models.Classinfo.objects.all()
    return render(request, 'portalteacher/allschoolresourcelist.html', 
                                        {'schools':schools,'classes':classes})

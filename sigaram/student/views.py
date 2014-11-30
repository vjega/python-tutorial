# -*- coding: utf-8 -*-
from django.utils.translation import (ugettext as _, activate)
from django.shortcuts import render
from student import models
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
        "link" : u"resourcetype",
        "caption": _("Deliverables"),
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
        "link" : u"studentresourcetype",
        "caption": _("Notes"),
        "stat": 125
        },{
        "color": u"red",
        "icon" : u"pencil",
        "link" : u"studentresourcetype",
        "caption": _("Written Work"),
        "stat": 125
        },
        {
        "color": u"green",
        "icon" : u"desktop",
        "link" : u"studentresourcetype",
        "caption": _("Practicals"),
        "stat": 125
        }]

    recent_acitivity_head = [_("Sl No."),_("Assignments"),_("Date")]
    admin_folders = models.AdminFolders.objects.all()
    recent_activity_body = models.Activitylog.recentactivities()
    recent_activities = {'head':recent_acitivity_head,
                         'body':recent_activity_body}
    return  render(request, 'portalstudent/index.html', {"folders":folders,
                                           "admin_folders":admin_folders,
                                           "recent_activities":recent_activities
                                           })
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

@switchlanguage
def resourcetype(request):
    folders = [{
        "id": "1",
        "name" :"Reading",
        "href" :"assignedresourcelist"
        },{
        "id": "2",
        "name" :"Image dialog",
        "href" :""
        },{
        "id": "3",
        "name" :"Writing board",
        "href" :""
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalstudent/resource_type.html', 
                  {"folders":folders,'resourcetype':resourcetype})

@switchlanguage
def workspace(request):
    folders = [{
        "id": "1",
        "name" :"Character",
        "href" :""
        },{
        "id": "2",
        "name" :"Photography",
        "href" :""
        },{
        "id": "3",
        "name" :"Lyrics",
        "href" :""
        },{
        "id": "4",
        "name" :"Video",
        "href" :""
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalstudent/workspace.html', 
                  {"folders":folders,'workspace':workspace})
@switchlanguage
def studentslist(request):
    user = models.Studentinfo.objects.filter(username=request.user.username)[0]
    return render(request, 'portalstudent/studentslist.html', {'user':user})

def assignedresourcelist(request):
    return render(request, 'portalstudent/assignedresourcelist.html')

def studentprofile(request):
    user = models.Studentinfo.objects.filter(username=request.user.username)[0]
    folders = [{
        "id"   :"1",
        "name" :"Deliverables",
        "href" :"studentassignedresourcelist"
        },{
        "id"   :"2",
        "name" :"Writing job",
        "href" :"viewstudentwrittenworks"
        }]
    return render(request, 'portalstudent/studentprofile.html', 
                  {"folders":folders, "user":user})

def studentassignedresourcelist(request):
    return render(request, 'portalstudent/studentassignedresourcelist.html')

def viewstudentresource(request):
    return render(request, 'portalstudent/viewstudentresource.html')

def viewstudentwrittenworks(request):
    return render(request, 'portalstudent/viewstudentwrittenworks.html')

def viewstudentwork(request):
    return render(request, 'portalstudent/viewstudentwork.html')
# -*- coding: utf-8 -*-
from django.utils.translation import (ugettext as _, activate)
from django.shortcuts import render
from teacher import models
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
    assignedresourcelist_head = [('Sl No.'),
                         _('Name'),
                         _('Short Name'),
                         _('Edit'),
                         _('Delete')]
    assignedresourcelist = {'head':assignedresourcelist_head}
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
    return render(request, 'portalteacher/viewworkspacelist.html', {'opt':request.GET.get('type')})

@switchlanguage
def writtenwork(request):
    return render(request, 'portalteacher/writtenwork.html')

@switchlanguage
def viewassessments(request):
    return render(request, 'portalteacher/viewassessments.html')
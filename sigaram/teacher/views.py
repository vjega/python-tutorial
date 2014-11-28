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
        "caption": _("Notes"),
        "stat": 125
        },{
        "color": u"red",
        "icon" : u"pencil",
        "caption": _("Written Work"),
        "stat": 125
        },
        {
        "color": u"green",
        "icon" : u"desktop",
        "caption": _("Practicals"),
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
        "name" :"எழுத்து",
        "href" :"workspacelist"
        },{
        "id": "2",
        "name" :"பல்லூடகம்",
        "href" :"workspacelist"
        },{
        "id": "3",
        "name" :"பாடல்",
        "href" :"workspacelist"
        },{
        "id": "4",
        "name" :"ஒளிப்படக்காட்சி",
        "href" :"workspacelist"
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portalteacher/workspace.html', 
                  {"folders":folders,'workspace':workspace})

@switchlanguage
def workspacelist(request):
    workspacelist_head = [('Sl No.'),
                         _('Name'),
                         _('Short Name'),
                         _('Edit'),
                         _('Delete')]
    workspacelist = {'head':workspacelist_head}
    return render(request, 'portalteacher/workspacelist.html')

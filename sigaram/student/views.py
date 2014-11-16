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
    return  render(request, 'portalstudent/index.html', {"folders":folders,
                                           "admin_folders":admin_folders,
                                           "recent_activities":recent_activities
                                           })

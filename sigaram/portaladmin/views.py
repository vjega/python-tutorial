# -*- coding: utf-8 -*-
from django.utils.translation import (ugettext as _, activate)
from django.shortcuts import render
from portaladmin import models
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
    return  render(request, 'portaladmin/index.html', {"folders":folders,
                                           "admin_folders":admin_folders,
                                           "recent_activities":recent_activities
                                           })

@switchlanguage
def adminlist(request):
    adminlist_head = [_('Sl No.'),
                         _('Photo'),
                         _('Name'),
                         _('User Name'),
                         _('Email Id'),
                         _('Delete')]
    adminlist_body = models.Admininfo.getlist()
    adminlist = {'head':adminlist_head, 'body':adminlist_body}
    return render(request, 'portaladmin/adminlist.html', {'adminlist':adminlist})

@switchlanguage
def teacherslist(request):
    schools = models.Schoolinfo.objects.all()
    """
    teacherslist_head = [('Sl No.'),
                         _('Photo'),
                         _('Name'),
                         _('User Name'),
                         _('Email Id'),
                         _('Edit'),
                         _('Delete')]
    teacherslist_body = models.Teacherinfo.getlist()
    teacherslist = {'head':teacherslist_head, 'body':teacherslist_body}
    """
    return render(request, 'portaladmin/teacherslist.html', {#'teacherslist':teacherslist,
                                                'schools':schools})

@switchlanguage
def studentslist(request):
    studentslist_head = [('Sl No.'),
                         _('Photo'),
                         _('Name'),
                         _('User Name'),
                         _('Email Id'),
                         _('Edit'),
                         _('Delete')]
    studentslist_body = models.Studentinfo.getlist()
    studentslist = {'head':studentslist_head, 'body':studentslist_body}
    return render(request, 'portaladmin/studentslist.html', {'studentslist':studentslist})

@switchlanguage
def schoollist(request):
    schoollist_head = [('Sl No.'),
                         _('Name'),
                         _('Short Name'),
                         _('Edit'),
                         _('Delete')]
    schoollist_body = models.Schoolinfo.objects.all()
    schoollist = {'head':schoollist_head, 'body':schoollist_body}
    return render(request, 'portaladmin/schoollist.html', {'schoollist':schoollist})

@switchlanguage
def teacherresourcelist(request):
    teacherresourcelist_head = [('Sl No.'),
                         _('Title'),
                         _('Date'),
                         _('Type'),
                         _('Delete')]
    teacherresourcelist_body = models.Teacherresourceinfo.objects.all()
    teacherresourcelist = {'head':teacherresourcelist_head, 
                           'body':teacherresourcelist_body}
    return render(request, 'portaladmin/teacherresourcelist.html', 
                  {'teacherresourcelist':teacherresourcelist})

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
    return render(request, 'portaladmin/studentresource_type.html', 
                  {"folders":folders,'studentresourcetype':studentresourcetype})

@switchlanguage
def resourcetype(request):
    folders = [{
        "id": "1",
        "name" :"வாசிப்பு",
        "href" :"portaladmin/subjectlist"
        },{
        "id": "2",
        "name" :"பட உரையாடல்",
        "href" :"portaladmin/subjectlist"
        },{
        "id": "3",
        "name" :"எழுத்து பலகை",
        "href" :"portaladmin/subjectlist"
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'portaladmin/resource_type.html', 
                  {"folders":folders,'resourcetype':resourcetype})

@switchlanguage
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


@switchlanguage
def subjectlist(request):
    folders = [{
        "id": "1",
        "name" :"{0} - 1 (0) ".format(_("Lession"))
        },{
        "id": "2",
        "name" :"{0} - 2 (2) ".format(_("Lession"))
        },{
        "id": "3",
       "name" :"{0} - 3 (12) ".format(_("Lession"))
        },{
        "id": "4",
       "name" :"{0} - 4 (15) ".format(_("Lession"))
        },{
        "id": "4",
       "name" :"{0} - 5 (15) ".format(_("Lession"))
        },{
        "id": "4",
       "name" :"{0} - 6 (15) ".format(_("Lession"))
        },{
        "id": "4",
       "name" :"{0} - 7 (15) ".format(_("Lession"))
        },{
        "id": "4",
       "name" :"{0} - 8 (15) ".format(_("Lession"))
        },{
        "id": "4",
       "name" :"{0} - 9 (15) ".format(_("Lession"))
        },{
        "id": "4",
       "name" :"{0} - 10 (15) ".format(_("Lession"))
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'subjectlist.html', 
                  {"folders":folders,'subjectlist':subjectlist})


@switchlanguage
def classlist(request):
    folders = [{
        "id": "1",
        "name" :"Primary1",
        "shortname" :"P1"
        },{
        "id": "2",
        "name" :"Primary2",
        "shortname" :"P2"
        },{
        "id": "3",
        "name" :"Primary3",
        "shortname" :"P3"
        },{
        "id": "4",
        "name" :"Primary4",
        "shortname" :"P4"
        },{
        "id": "5",
        "name" :"Primary5",
        "shortname" :"P5"
        },{
        "id": "6",
        "name" :"Primary6",
        "shortname" :"P6"
        }]
    classlist_head = [_('Sl No.'),
                      _('School Name'),
                      _('Short Name'),
                      _('Edit'),
                      _('Delete')]
    classlist = {'head':classlist_head}
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'classlist.html', 
                  {"folders":folders, 'classlist':classlist})

@switchlanguage
def statistics(request):
    studentslist_head = [_('Sl No.'),
                         _('Photo'),
                         _('Name'),
                         _('User Name'),
                         _('Edit')]
    studentslist_body = models.Studentinfo.getlist() 
    studentslist = {'head':studentslist_head, 'body':studentslist_body}
    return render(request, 'statistics.html', {'studentslist':studentslist})

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
    return render(request, 'classroom.html', {'studentslist':studentslist})

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
    return render(request, 'portaladmin/studentslist.html', {'studentslist':studentslist})

def mindmap(request):
    return render(request, 'mindmap.html', {})
    
def sticky_notes(request):
    return render(request, 'sticky_notes.html', {})
    
def calendar(request):
    return render(request, 'calendar.html', {})
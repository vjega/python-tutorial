# -*- coding: utf-8 -*-
from django.utils.translation import (ugettext as _, activate)
from django.shortcuts import render
from portaladmin import models

def home(request):
    #activate('ta')
    #request.session['django_language'] = 'ta'
    folders = [{
        "color": u"primary",
        "icon" : u"university",
        "link" : "schoollist",
        "caption": _("Schools"),
        "stat": 25
        }, {
        "color": u"green",
        "icon" : u"book",
        "link" : "teacherresourcelist",
        "caption": "{0} {1}".format(_("Teachers"),_("Resources")),
        "stat": 64
        }, {
        "color": u"yellow",
        "icon" : u"book",
        "link" : "studentresourcetype",
        "caption": "{0} {1}".format(_("Student"), _("Resources")),
        "stat": 125
        }]

    recent_acitivity_head = [_("Sl No."),u'வேலைகள்',_("Date")]
    admin_folders = models.AdminFolders.objects.all()
    recent_activity_body = models.Activitylog.recentactivities()
    recent_activities = {'head':recent_acitivity_head,
                         'body':recent_activity_body}
    return  render(request, 'index.html', {"folders":folders,
                                           "admin_folders":admin_folders,
                                           "recent_activities":recent_activities
                                           })

def adminlist(request):
    adminlist_head = [u'எண்',u'புகைப்படம்',u'பெயர்',u'பயனர்பெயர்',u'மின்னஞ்சல்','நீக்கு']
    adminlist_body = models.Admininfo.getlist()
    adminlist = {'head':adminlist_head, 'body':adminlist_body}
    return render(request, 'adminlist.html', {'adminlist':adminlist})

def teacherslist(request):
    teacherslist_head = [u'எண்',u'புகைப்படம்',u'பெயர்',u'பயனர்பெயர்',u'மின்னஞ்சல்','மாற்று','நீக்கு']
    teacherslist_body = models.Teacherinfo.getlist()
    teacherslist = {'head':teacherslist_head, 'body':teacherslist_body}
    return render(request, 'teacherslist.html', {'teacherslist':teacherslist})

def studentslist(request):
    studentslist_head = [u'எண்',u'புகைப்படம்',u'பெயர்',u'பயனர்பெயர்',u'மின்னஞ்சல்','மாற்று','நீக்கு']
    studentslist_body = models.Studentinfo.getlist()
    studentslist = {'head':studentslist_head, 'body':studentslist_body}
    return render(request, 'studentslist.html', {'studentslist':studentslist})

def schoollist(request):
    schoollist_head = [u'எண்',u'பள்ளியின் பெயர்',
                       u'குறும் பெயர்',u'மாற்று',u'நீக்கு']
    schoollist_body = models.Schoolinfo.objects.all()
    schoollist = {'head':schoollist_head, 'body':schoollist_body}
    return render(request, 'schoollist.html', {'schoollist':schoollist})

def teacherresourcelist(request):
    teacherresourcelist_head = [u'எண்',u'தலைப்பு',
                                u'நாள்',u'வகை',u'நீக்கு']
    teacherresourcelist_body = models.Teacherresourceinfo.objects.all()
    teacherresourcelist = {'head':teacherresourcelist_head, 
                           'body':teacherresourcelist_body}
    return render(request, 'teacherresourcelist.html', 
                  {'teacherresourcelist':teacherresourcelist})

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
    return render(request, 'studentresource_type.html', 
                  {"folders":folders,'studentresourcetype':studentresourcetype})

def resourcetype(request):
    folders = [{
        "id": "1",
        "name" :"வாசிப்பு",
        "href" :"subjectlist"
        },{
        "id": "2",
        "name" :"பட உரையாடல்",
        "href" :"subjectlist"
        },{
        "id": "3",
        "name" :"எழுத்து பலகை",
        "href" :"subjectlist"
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'resource_type.html', 
                  {"folders":folders,'resourcetype':resourcetype})

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


def subjectlist(request):
    folders = [{
        "id": "1",
        "name" :"பாடம் - 1 (0) "
        },{
        "id": "2",
        "name" :"பாடம் - 2 (2) "
        },{
        "id": "3",
       "name" :"பாடம் - 3 (12) "
        },{
        "id": "4",
       "name" :"பாடம் - 4 (15) "
        },{
        "id": "4",
       "name" :"பாடம் - 5 (15) "
        },{
        "id": "4",
       "name" :"பாடம் - 6 (15) "
        },{
        "id": "4",
       "name" :"பாடம் - 7 (15) "
        },{
        "id": "4",
       "name" :"பாடம் - 8 (15) "
        },{
        "id": "4",
       "name" :"பாடம் - 9 (15) "
        },{
        "id": "4",
       "name" :"பாடம் - 10 (15) "
        }]
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'subjectlist.html', 
                  {"folders":folders,'subjectlist':subjectlist})


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
    classlist_head = [u'எண்',u'பள்ளியின் பெயர்',
                       u'குறும் பெயர்',u'மாற்று',u'நீக்கு']
    classlist = {'head':classlist_head}
    #studentresourcetype_body = models.Teacherresourceinfo.objects.all()
    #studentresourcetype = {'head':studentresourcetype_head, 
                           #'body':studentresourcetype_body}
    return render(request, 'classlist.html', 
                  {"folders":folders, 'classlist':classlist})

def statistics(request):
    studentslist_head = [u'எண்',u'புகைப்படம்',u'பெயர்',u'பயனர்பெயர்',u'மின்னஞ்சல்']
    studentslist_body = models.Studentinfo.getlist() 
    studentslist = {'head':studentslist_head, 'body':studentslist_body}
    return render(request, 'statistics.html', {'studentslist':studentslist})

def classroom(request):
    studentslist_head = [u'எண்',u'புகைப்படம்',u'பெயர்',u'பயனர்பெயர்',u'மின்னஞ்சல்','மாற்று','நீக்கு']
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

def billboard(request):
    studentslist_head = [u'எண்',u'புகைப்படம்',u'பெயர்',u'பயனர்பெயர்',u'மின்னஞ்சல்','மாற்று','நீக்கு']
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
    return render(request, 'studentslist.html', {'studentslist':studentslist})

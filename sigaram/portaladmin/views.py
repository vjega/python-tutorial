# -*- coding: utf-8 -*-
from django.shortcuts import render
from portaladmin import models

# Create your views here.
def home(request):
    folders = [{
        "color": u"primary",
        "icon" : u"building",
        "link" : "schoollist",
        "caption": u"பள்ளிகள்",
        "stat": 25
        }, {
        "color": u"green",
        "icon" : u"book",
        "link" : "teacherresourcelist",
        "caption": u"ஆசிரியர் வளங்கள்",
        "stat": 64
        }, {
        "color": u"yellow",
        "icon" : u"graduation-cap",
        "link" : "studentresource_type",
        "caption": u"மாணவர் வளங்கள்",
        "stat": 125
        }]
    recent_acitivity_head = [u'எண்',u'வேலைகள்',u'நாள்']
    recent_activity_body = models.Activitylog.recentactivities()
    recent_activities = {'head':recent_acitivity_head,
                         'body':recent_activity_body}
    return  render(request, 'index.html', {"folders":folders, 
                                           'recent_activities':recent_activities
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


def statisticsstudentslist(request):
    statisticsstudentslist_head = [u'எண்',u'புகைப்படம்',
                                u'பெயர்',u'பயனர் பெயர்',u'மின்னஞ்சல்']
    statisticsstudentslist_body = models.Studentinfo.getlist()
    statisticsstudentslist = {'head':statisticsstudentslist_head, 
                           'body':statisticsstudentslist_body}
    return render(request, 'statisticsstudentslist.html', 
                  {'statisticsstudentslist':statisticsstudentslist})

def studentresource_type(request):
    studentresource_type_head = [u'எண்',u'தலைப்பு',
                                u'நாள்',u'வகை',u'நீக்கு']
    studentresource_type_body = models.Teacherresourceinfo.objects.all()
    studentresource_type = {'head':studentresource_type_head, 
                           'body':studentresource_type_body}
    return render(request, 'studentresource_type.html', 
                  {'studentresource_type':studentresource_type})


def statistics(request):
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
from django.utils.translation import (ugettext as _, activate)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from portaladmin import models
from forum.forms import (ForumsForm,
						NewtopicForm,
						NewpostForm)

def index(request):
    return render(request, 'portalforum/index.html')

def forum(request):
    return render(request, 'portalforum/forum.html', {"form" : ForumsForm.ForumsForm()})

def viewtopic(request):
   foruminfo = models.Foruminfo.objects.all()
   return render(request, 'portalforum/viewtopic.html',{"form" : NewtopicForm.NewtopicForm()})

def viewpost(request):
    return render(request, 'portalforum/viewpost.html',{"form" : NewpostForm.NewpostForm()})

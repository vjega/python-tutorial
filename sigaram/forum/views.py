from django.utils.translation import (ugettext as _, activate)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from forum import models
from forum.forms import (ForumsForm)

def index(request):
    return render(request, 'portalforum/index.html', {"form" : ForumsForm.ForumsForm()})

def viewtopic(request):
   return render(request, 'portalforum/viewtopic.html')

def viewpost(request):
    return render(request, 'portalforum/viewpost.html')

from django.utils.translation import (ugettext as _, activate)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from portaladmin import models

def index(request):
    return render(request, 'portalforum/index.html')

from django.shortcuts import (render, redirect)
from django.http import HttpResponse

# Create your views here.
def home(request):
    return  HttpResponse("Hello Admin Page")

def logout(request):
    return HttpResponse("Logging Out of the system")

def forum(request):
    return HttpResponse("Forum module will be taken up later")

    
def togglelanguage(request):
    """
    """
    if request.session.get("django_language") == 'en':
        request.session["django_language"] = 'ta'
    elif request.session.get("django_language") == 'ta':
        request.session["django_language"] = 'en'
    
    return redirect(request.META.get('HTTP_REFERER','/admin/home/'))
     

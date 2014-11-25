from django.shortcuts import (render, redirect)
from django.http import HttpResponse

# Create your views here.
def home(request):
    return redirect('/admin/home')

def logout(request):
    return HttpResponse("Logging Out of the system")

def forum(request):
    return HttpResponse("Forum module will be taken up later")

    
def togglelanguage(request):
    """
    """
    print request.session.get("django_language")
    if request.session.get("django_language", 'en') == 'en':
        request.session["django_language"] = 'ta'
    elif request.session.get("django_language") == 'ta':
        request.session["django_language"] = 'en'
    
    return redirect(request.META.get('HTTP_REFERER','/admin/home/'))
     

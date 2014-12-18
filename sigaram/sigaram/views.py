from django.shortcuts import (render, redirect)
from django.http import HttpResponse
from django.views.generic import FormView
from ajaxuploader.views import AjaxFileUploader

#an imported view function from ajaxuplod
import_uploader = AjaxFileUploader()

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
     
def user_landing(request):
    if str(request.user) == "AnonymousUser": 
        return redirect('/login')
    
    try:
        group = request.user.groups.all()[0].name
    except Exception as e:
        raise(Http404)

    if group == 'Teacher':
        return redirect('/teacher/home')
    elif group == 'Student':
        return redirect('/student/home')
    elif group == 'Admin':
        return redirect('/admin/home')
    else:
        return redirect('/404')
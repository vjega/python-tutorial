from django.shortcuts import (render, redirect)
from django.http import HttpResponse
from django.views.generic import FormView

def home(request):
    return user_landing(request)

def logout(request):
    return HttpResponse("Logging Out of the system")

def forum(request):
    return HttpResponse("Forum module will be taken up later")

def billboard(request):
    return HttpResponse("Billboard module will be taken up later")
    
def togglelanguage(request):
    """
    """
    print request.session.get("django_language")
    if request.session.get("django_language", 'en') == 'en':
        request.session["django_language"] = 'ta'
    elif request.session.get("django_language") == 'ta':
        request.session["django_language"] = 'en'
    else:
        request.session["django_language"] = 'ta'

    return redirect(request.META.get('HTTP_REFERER','/admin/home/'))
     
def user_landing(request):
    if str(request.user) == "AnonymousUser": 
        return redirect('/login')
    
    try:
        group = request.user.groups.all()[0].name
    except Exception as e:
        raise(Http404)

    if group == 'Teacher':
        from portaladmin.models import Teacherinfo
        # from portaladmin.models import bulletinmappinginfo
        t = Teacherinfo.objects.filter(username=request.user.username)[0]
        request.session['schoolid'] = t.schoolid
        request.session['classid'] =  t.classid
        request.session['section'] =  t.section
        return redirect('/teacher/home')
    elif group == 'Student':
        from portaladmin.models import Studentinfo
        t = Studentinfo.objects.filter(username=request.user.username)[0]
        request.session['schoolid'] = request.session['stu_schoolid'] = t.schoolid
        request.session['classid']  = request.session['stu_classid']  = t.classid
        request.session['section']  = request.session['stu_section']  = t.section
        return redirect('/student/home')

    elif group == 'Admin':
        return redirect('/admin/home')
    else:
        return redirect('/404')
import json
from django.contrib.auth.models import User, Group
from portaladmin import models

def create_login(group):
    def outer(f):
        def inner(obj, request):
            admindata =  json.loads(request.DATA.keys()[0])
            user = User.objects.create_user(admindata.get('username'), 
                                            email=admindata.get('emailid'), 
                                            password=admindata.get('password'),
                                            first_name=admindata.get('firstname'),
                                            last_name='') #admindata.get('lastname'))
            g = Group.objects.get(name=group) 
            g.user_set.add(user)
            return f(obj, request)
        return inner
    return outer

def inactivate_user(f):
    def inner(obj, request, pk):
        return f(obj, request, pk)
    return inner

def delete_login(group):
    def outer(f):
        def inner(obj, request, pk):
            if group == 'Admin':
                print pk
                u = models.Admininfo.objects.get(pk=pk)
            elif group == 'Teacher':
                u = models.Teacherinfo.objects.get(pk=pk)
            elif group == 'Student':
                u = models.Studentinfo.objects.get(pk=pk)
            
            login = User.objects.filter(username=u.username)[0]
            login.delete()
            return f(obj, request, pk)
        return inner
    return outer

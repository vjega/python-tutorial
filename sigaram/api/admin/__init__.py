import json
from django.contrib.auth.models import User, Group
def create_login(group):
    def outer(f):
        def inner(obj, request):
            admindata =  json.loads(request.DATA.keys()[0])
            user = User.objects.create_user(admindata.get('username'), 
                                            email=admindata.get('emailid'), 
                                            password=admindata.get('password'),
                                            first_name=admindata.get('firstname'),
                                            last_name=admindata.get('lastname'))
            g = Group.objects.get(name=group) 
            g.user_set.add(user)
            return f(obj, request)
        return inner
    return outer


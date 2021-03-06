#!/home/excelasia/.virtualenvs/portal/bin/python
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sigaram.settings")
django.setup()

from portaladmin import models
from django.contrib.auth.models import User, Group

import logging
logging.basicConfig(filename='error.log',level=logging.ERROR)

def add_user(username, password, firstname, lastname='', g=1):
    user = User.objects.create_user(username, email=None, password=password,
                first_name=firstname, last_name=lastname)
    
    
    if int(g) == 0:
        group = 'Admin'
    elif int(g) == 1:
        group = 'Student'
    elif int(g) == 2:
        group = 'Teacher'
    print group
    f = Group.objects.get(name=group) 
    f.user_set.add(user)
    
def main():
    li = models.Studentinfo.objects.filter(isdelete=3)
    for k, u in enumerate(li):
        print '-'*10
        print k
        print u.username
        print u.firstname
        print u.lastname
        #print u.usertype
        print u.password
        print '*'*10
        try :
            add_user(u.username, u.password, u.firstname)
        except Exception as e:
            logging.error(u.username)
            logging.error(e)

if __name__ == '__main__':
    main()

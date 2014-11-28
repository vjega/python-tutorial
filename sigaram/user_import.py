#!/Users/jega/.virtualenvs/portal/bin/python
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sigaram.settings")
django.setup()

from portaladmin import models
from django.contrib.auth.models import User, Group

import logging
logging.basicConfig(filename='error.log',level=logging.ERROR)

def add_user(username, password, firstname, lastname, group):
    user = User.objects.create_user(username, email=None, password=password,
                first_name=firstname, last_name=lastname)
    user.groups.add(group)

def main():
    li = models.Logininfo.objects.filter(isdelete=0)
    for k, u in enumerate(li):
        print '-'*10
        print k
        print u.username
        print u.firstname
        print u.lastname
        print u.usertype
        print u.password
        print '*'*10
        try :
            add_user(u.username, u.password, u.firstname, u.lastname, u.usertype)
        except Exception as e:
            logging.error(u.username)
            logging.error(e)

if __name__ == '__main__':
    main()
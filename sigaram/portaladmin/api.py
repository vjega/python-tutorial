'''
from portaladmin import models as m
from rest_framework import viewsets
#from rest_framework import ModelResource

class AdminFoldersResource(viewsets.ModelResource):
    class Meta:
        queryset = m.AdminFolders.objects.all()
        resource_name = 'adminfolders'

class AdminInfoResource(viewsets.ModelResource):
    class Meta:
        queryset = m.Admininfo.objects.all()
        resource_name = 'admininfo'

    def dehydrate(self, bundle):
        sql = """SELECT ai.adminid,
                   ai.firstname,
                   ai.lastname,
                   ai.username,
                   ai.emailid,
                   ai.imageurl 
            FROM `admininfo` ai
            INNER JOIN logininfo li on li.username=ai.username 
            WHERE li.isdelete=0 
            ORDER BY adminid""";
        qs = m.Admininfo.objects.raw(sql)
        return [row for row in qs]
        #return qs
'''
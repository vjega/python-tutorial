#from django.db import models

from __future__ import unicode_literals

from django.db import (models, 
                       connection)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class Activitylog(models.Model):
    activityid = models.BigIntegerField(primary_key=True)
    loginid = models.BigIntegerField()
    pagename = models.CharField(max_length=1000)
    operation = models.CharField(max_length=500)
    usertype = models.IntegerField()
    stringsentence = models.CharField(max_length=2000)
    updateddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'activitylog'

    @staticmethod
    def recentactivities():
        sql = """SELECT operation,
                    stringsentence,
                    updateddate 
            FROM activitylog al
            INNER JOIN logininfo li ON li.loginid = al.loginid 
            -- WHERE al.loginid = {$loginid} 
            ORDER by activityid DESC 
            LIMIT 10""";
        cursor = connection.cursor()
        cursor.execute(sql)
        return dictfetchall(cursor)

class AdminFolders(models.Model):
    folder_id = models.IntegerField(primary_key=True)
    folder_name = models.CharField(max_length=200)
    folder_description = models.CharField(max_length=1000)
    added_date = models.DateTimeField()
    folder_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_folders'




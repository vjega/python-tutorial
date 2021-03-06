# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
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
        sql = """
        SELECT  DISTINCT operation,
                stringsentence,
                updateddate,
                CONCAT(au.first_name,' ',au.last_name) as name
        FROM activitylog al
        INNER JOIN auth_user au ON au.username = al.loginid 
        -- WHERE al.loginid = {$loginid} 
        ORDER by updateddate DESC 
        LIMIT 100""";
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

class Studentinfo(models.Model):
    studentid = models.BigIntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=50)
    imageurl = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    emailid = models.CharField(max_length=100)
    schoolid = models.BigIntegerField()
    classid = models.BigIntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'studentinfo'
        
    @staticmethod
    def getlist():
        sql = """SELECT si.studentid,
                       si.firstname,
                       si.username,
                       si.emailid,
                       si.classid,
                       si.imageurl 
                FROM studentinfo si
                INNER JOIN logininfo li ON li.username=si.username 
                WHERE schoolid = 0 AND 
                     classid = 1 AND 
                    si.isdelete=0 
                ORDER BY studentid"""
        cursor = connection.cursor()
        cursor.execute(sql)
        return dictfetchall(cursor)

class Studentworkspaceinfo(models.Model):
    workspaceid = models.BigIntegerField(primary_key=True)
    workspacetitle = models.CharField(max_length=500)
    workspacetype = models.CharField(max_length=200)
    workspacetext = models.TextField()
    documenturl = models.CharField(max_length=1000)
    imageurl = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=1000)
    audiourl = models.CharField(max_length=1000)
    classid = models.BigIntegerField()
    schoolid = models.BigIntegerField()
    isassigned = models.IntegerField()
    isapproved = models.IntegerField()
    isdeleted = models.IntegerField()
    resourceid = models.IntegerField()
    postedby = models.BigIntegerField()
    posteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'studentworkspaceinfo'
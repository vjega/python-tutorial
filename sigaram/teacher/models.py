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

class Teacherresourceinfo(models.Model):
    teacherresourceid = models.BigIntegerField(primary_key=True)
    classid = models.IntegerField()
    section = models.CharField(max_length=1)
    chapterid = models.IntegerField()
    resourcetype = models.CharField(max_length=200)
    resourcecategory = models.IntegerField()
    originaltext = models.TextField(db_column='originalText')  # Field name made lowercase.
    resourcetitle = models.CharField(max_length=1000)
    resourcedescription = models.TextField()
    documenturl = models.CharField(max_length=1000)
    imageurl = models.CharField(max_length=1000)
    audiourl = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=1000)
    schoolid = models.IntegerField()
    isapproved = models.IntegerField()
    isdeleted = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'teacherresourceinfo'

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

class Schoolinfo(models.Model):
    schoolid = models.BigIntegerField(primary_key=True)
    schoolname = models.CharField(max_length=500)
    shortname = models.CharField(max_length=400)
    description = models.CharField(max_length=1000)
    schoolimageurl = models.CharField(max_length=1000)
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'schoolinfo'

class Classinfo(models.Model):
    classid = models.BigIntegerField(primary_key=True)
    classname = models.CharField(max_length=500)
    shortname = models.CharField(max_length=500)
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'classinfo'

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
    isdelete = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'studentinfo'

class Workspaceinfo(models.Model):
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
    postedby = models.BigIntegerField()
    posteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'workspaceinfo'

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
               --  WHERE -- schoolid = {selectedschoolid} AND 
                    -- classid = {classid} AND 
                   --  isdelete=0 
                ORDER BY studentid"""
        cursor = connection.cursor()
        cursor.execute(sql)
        return dictfetchall(cursor)



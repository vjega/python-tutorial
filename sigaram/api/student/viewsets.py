from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from django.db import connection
from portaladmin import models
from django.db import connection
import studentserializers
import json, time

class studentViewSet(viewsets.ModelViewSet):
    queryset = models.Studentinfo.objects.all()
    serializer_class = studentserializers.StudentinfoSerializer
    
    def list(self, request):
        schoolid =  request.GET.get('schoolid')
        classid  =  request.GET.get('classid')

        if schoolid and classid:
            queryset = models.Studentinfo.objects.filter(schoolid=schoolid, classid=classid)
        elif schoolid:
            queryset = models.Studentinfo.objects.filter(schoolid=schoolid)
        else:
            queryset = models.Studentinfo.objects.all()
        
        serializer = studentserializers.StudentinfoSerializer(queryset, many=True)
        return Response(serializer.data)
    def update(self, request, pk=None):
        student = models.Studentinfo.objects.get(pk=pk)
        data = json.loads(request.DATA.keys()[0])
        student.firstname = data.get('username')
        student.lastname = data.get('lastname')
        student.emailid = data.get("emailid")
        student.save()
        return Response(request.DATA)

class ResourceinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Resourceinfo.objects.all()
    serializer_class = studentserializers.ResourceinfoSerializer
    
    def list(self, request):
        studentid   = request.GET.get('studentid')
        sql ="""
            SELECT  ri.resourceid,
                    ri.resourcetitle,
                    date(ari.assigneddate) as createddate,
                    ri.resourcetype,
                    ri.thumbnailurl,
                    ari.studentid
            FROM resourceinfo ri
            INNER JOIN assignresourceinfo ari on ari.resourceid=ri.resourceid
            WHERE ri.isdeleted=0  
            and ari.studentid='%s'
            AND isanswered=1 
            GROUP BY ri.resourceid 
            ORDER BY ari.assigneddate DESC 
        """ % studentid
        cursor = connection.cursor()
        # print sql
        #cursor.execute(sql, loginname_to_userid('Student', request.user.username))
        cursor.execute(sql)
        #cursor.execute(sql, "3680")
        #print dir(cursor)
        #result = cursor.fetchall()
        #print return [
        
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

class WrittenworkinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Writtenworkinfo.objects.all()
    serializer_class = studentserializers.WrittenworkinfoSerializer

class Studentworkspaceinfo(viewsets.ModelViewSet):

    queryset = models.Studentworkspaceinfo.objects.all()
    serializer_class = studentserializers.StudentworkspaceinfoSerializer

    def list(self, request):
        workspacetype   = request.GET.get('workspacetype')
        kwarg = {}
        kwarg['isdeleted'] = 0
        if workspacetype:
            kwarg['workspacetype'] = workspacetype
        
        
        queryset = models.Studentworkspaceinfo.objects.filter(**kwarg).order_by('-posteddate')
        serializer = studentserializers.StudentworkspaceinfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        student = models.Studentinfo.objects.filter(username = request.user.username)[0]
        studentwork = models.Studentworkspaceinfo()
        studentworkdata =  json.loads(request.DATA.keys()[0])
        studentwork.workspacetitle = studentworkdata.get('workspacetitle')
        studentwork.workspacetype = studentworkdata.get('workspacetype')
        studentwork.workspacetext = studentworkdata.get('workspacetext')
        studentwork.classid = student.classid #studentworkdata.get('classid')
        studentwork.schoolid = student.schoolid #studentworkdata.get('schoolid')
        studentwork.isassigned = 0
        studentwork.isapproved = 0
        studentwork.isdeleted = 0
        studentwork.resourceid = student.studentid
        studentwork.postedby = request.user.id
        studentwork.posteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        studentwork.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class StudentnotesinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Notesinfo.objects.all()
    serializer_class = studentserializers.StudentnotesinfoSerializer

    def list(self, request):
        userid =  request.user.id
        if userid :
            queryset = models.Notesinfo.objects.filter(createdby=userid).order_by('-createddate')
        else:
            queryset = models.Notesinfo.objects.all().order_by('-createddate')
        serializer = studentserializers.StudentnotesinfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        studentnotes = models.Notesinfo()
        studentnotesdata =  json.loads(request.DATA.keys()[0])
        studentnotes.notestitle = studentnotesdata.get('notestitle')
        studentnotes.notes = studentnotesdata.get('notes')
        studentnotes.isdeleted = 0
        studentnotes.createdby = request.user.id
        studentnotes.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        studentnotes.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class Studentbulletinboardlist(viewsets.ModelViewSet):
    queryset = models.Bulletinboardinfo.objects.all()
    serializer_class = studentserializers.StudentBulletinboardlistinfoSerializer

    def list(self, request):
        student = request.user.username
        print student
        stu = models.Studentinfo.objects.filter(username=student)
        schoolid = stu[0].schoolid
        sql = """
        SELECT  bi.bulletinboardid, 
                bi.messagetitle,
                bi.message,
                bmi.schoolid,
                DATE(bi.posteddate ) AS posteddate
        FROM bulletinboardinfo bi
        INNER JOIN bulletinmappinginfo bmi ON bmi.bulletinboardid = bi.bulletinboardid
        WHERE bmi.schoolid = %s
        GROUP BY bi.bulletinboardid
        """ % schoolid
        cursor = connection.cursor()
        #print sql
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

    def create(self, request):
        data = json.loads(dict(request.DATA).keys()[0])
        #Saving annoucement
        bbi = models.Bulletinboardinfo()
        bbi.messagetitle = data.get('messagetitle')
        bbi.message = data.get('message')
        bbi.attachmenturl = data.get('attachmenturl')
        if data.get('cattype') == 'schools':
            bbi.schoolid = data.get('schoolid')
        else:
            bbi.schoolid = 0 #data.get('schoolid')
        bbi.classid = data.get('classid',0)
        bbi.isrecord = data.get('isrecord',0)
        bbi.postedby = request.user.id
        bbi.posteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        bbi.save()
        bbiid = bbi.bulletinboardid
        #print bbi.bulletinboardid
       
        return Response(request.DATA)

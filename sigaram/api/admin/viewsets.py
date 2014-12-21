from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
import json, time
from django.db.models import Q
from api.admin import (create_login, 
                       delete_login)
from django.db.models import Q
from django.db import connection
from portaladmin import models
import  adminserializers

def loginname_to_userid(usertype, username):

    if usertype =='Admin':
        m = models.Admininfo.objects.filter(username=username)[0]
        return m.adminid
    elif usertype =='Teacher':
        m = models.Teacherinfo.objects.filter(username=username)[0]
        return m.teacherid
    elif usertype =='Student':
        m = models.Studentinfo.objects.filter(username=username)[0]
        return m.studentid


class AdmininfoViewSet(viewsets.ModelViewSet):

    queryset = models.Admininfo.objects.filter(isdelete=0)
    serializer_class = adminserializers.AdminInfoSerializer

    @create_login('Admin')
    def create(self, request):
        admin = models.Admininfo()
        admindata =  json.loads(request.DATA.keys()[0])
        admin.username = admindata.get('username')
        admin.firstname = admindata.get('firstname')
        admin.lastname = admindata.get('lastname')
        admin.emailid = admindata.get('emailid')
        admin.imageurl = admindata.get('image')
        admin.isdelete = 0
        admin.createdby = request.user.id
        admin.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        admin.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    @delete_login('Admin')
    def destroy(self, request, pk):
        print pk
        models.Admininfo.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

class AdminFoldersViewSet(viewsets.ModelViewSet):

    queryset = models.AdminFolders.objects.all()
    serializer_class = adminserializers.AdminFolderSerializer

class teacherViewSet(viewsets.ModelViewSet):
    queryset = models.Teacherinfo.objects.all()
    serializer_class = adminserializers.TeacherinfoSerializer
    def list(self, request):
        schoolid =  request.GET.get('schoolid')
        if schoolid :
            queryset = models.Teacherinfo.objects.filter(schoolid=schoolid)
        else:
            queryset = models.Teacherinfo.objects.all()
        serializer = adminserializers.TeacherinfoSerializer(queryset, many=True)
        return Response(serializer.data)

    @create_login('Teacher')
    def create(self, request):
        teacher = models.Teacherinfo()
        teacherdata =  json.loads(request.DATA.keys()[0])
        teacher.username = teacherdata.get('username')
        teacher.lastname = teacherdata.get('lastname')
        teacher.password = teacherdata.get('password')
        teacher.firstname = teacherdata.get('firstname')
        teacher.schoolid = teacherdata.get('schoolid')
        teacher.classid = '1' #teacherdata.get('classid')
        teacher.emailid = teacherdata.get('emailid')
        teacher.imageurl = teacherdata.get('imageurl')
        #teacher.imageurl = studentdata.get('imageurl')
        teacher.isdelete = 0
        teacher.createdby = request.user.id
        teacher.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        teacher.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        teacher = models.Teacherinfo.objects.get(pk=pk)
        teacherdata =  json.loads(request.DATA.keys()[0])
        teacher.username = teacherdata.get('username')
        teacher.lastname = teacherdata.get('lastname')
        teacher.password = teacherdata.get('password')
        teacher.firstname = teacherdata.get('firstname')
        teacher.schoolid = teacherdata.get('schoolid')
        #teacher.classid = '1' #teacherdata.get('classid')
        teacher.emailid = teacherdata.get('emailid')
        teacher.save()
        return Response(request.DATA)

    @delete_login('Teacher')
    def destroy(self, request, pk):
        teacher = models.Teacherinfo.objects.get(pk=pk)
        teacher.isdelete = 1
        teacher.save()
        return Response('"msg":"delete"')


class studentViewSet(viewsets.ModelViewSet):
    queryset = models.Studentinfo.objects.filter(isdelete=0)
    serializer_class = adminserializers.StudentinfoSerializer
    
    def list(self, request):
        schoolid =  request.GET.get('schoolid')
        classid  =  request.GET.get('classid')
        schoolids  =  request.GET.get('schoolids')

        if schoolid and classid:
            queryset = models.Studentinfo.objects.filter(schoolid=schoolid, classid=classid)
        elif schoolid:
            queryset = models.Studentinfo.objects.filter(schoolid=schoolid)
        elif schoolids:
            schools = schoolids.split(",")
            q = Q() 
            for s in schools:
                q |= Q(schoolid=s) 
            queryset = models.Studentinfo.objects.filter(q, classid=classid)
        else:
            queryset = models.Studentinfo.objects.all()
        
        serializer = adminserializers.StudentinfoSerializer(queryset, many=True)
        return Response(serializer.data)
       
    @create_login('Student')   
    def create(self, request):
        student = models.Studentinfo()
        studentdata =  json.loads(request.DATA.keys()[0])
        student.schoolid = studentdata.get('schoolid')
        student.classid = studentdata.get('classid')
        student.username = studentdata.get('username')
        student.password = studentdata.get('password')
        student.firstname = studentdata.get('firstname')
        student.lastname = studentdata.get('lastname')
        student.emailid = studentdata.get('emailid')
        student.imageurl = studentdata.get('imageurl')
        student.isdelete = 0
        student.createdby = request.user.id
        student.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        student.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        student = models.Studentinfo.objects.get(pk=pk)
        studentdata =  json.loads(request.DATA.keys()[0])
        student.username = studentdata.get('username')
        student.lastname = studentdata.get('lastname')
        student.password = studentdata.get('password')
        student.firstname = studentdata.get('firstname')
        student.schoolid = studentdata.get('schoolid')
        student.emailid = studentdata.get('emailid')
        student.imageurl = studentdata.get('imageurl')
        student.save()
        return Response(request.DATA)

    @delete_login('Student')
    def destroy(self, request, pk=None):
        student = models.Studentinfo.objects.get(pk=pk)
        student.isdelete = 1
        student.save()
        return Response('"msg":"delete"')

class TeacherResourcesViewSet(viewsets.ModelViewSet):
    queryset = models.TeacherResources.objects.all()
    serializer_class = adminserializers.TeacherResourcesSerializer
    
    def list(self, request):
        resource_folder_id =  request.GET.get('resource_folder_id')

        if resource_folder_id:
            queryset = models.TeacherResources.objects.filter(resource_folder_id=resource_folder_id)
        else:
            queryset = models.TeacherResources.objects.all()
        
        serializer = adminserializers.TeacherResourcesSerializer(queryset, many=True)
        return Response(serializer.data)

class TeacherresourceinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Teacherresourceinfo.objects.all()
    serializer_class = adminserializers.TeacherresourceinfoSerializer

    def create(self, request):
        teacherresource = models.Teacherresourceinfo()
        teacherresourcedata =  json.loads(request.DATA.keys()[0])
        restype = teacherresourcedata.get('resourcetype')
        teacherresource.schoolid = teacherresourcedata.get('schoolid')
        teacherresource.classid = teacherresourcedata.get('classid')
        teacherresource.section = teacherresourcedata.get('section')
        teacherresource.resourcetype = restype
        teacherresource.resourcetitle = teacherresourcedata.get('resourcetitle')
        teacherresource.documenturl = "" #teacherresourcedata.get('documenturl')
        teacherresource.imageurl = "" #teacherresourcedata.get('imageurl')
        teacherresource.audiourl = "" #teacherresourcedata.get('audiourl')
        teacherresource.videourl = "" #teacherresourcedata.get('videourl')
        if restype == "text":
            teacherresource.documenturl = teacherresourcedata.get('fileurl')
        elif restype == "audio":
            teacherresource.audiourl = teacherresourcedata.get('fileurl')
        elif restype == "image":
            teacherresource.imageurl = teacherresourcedata.get('fileurl')
        elif restype == "video":
            teacherresource.videourl = teacherresourcedata.get('fileurl')
        teacherresource.resourcecategory = teacherresourcedata.get('resourcecategory')
        teacherresource.chapterid = teacherresourcedata.get('chapterid')
        teacherresource.createdby = request.user.id
        teacherresource.isapproved = 0
        teacherresource.isdeleted = 0
        teacherresource.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        teacherresource.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')
    

class ResourceinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Resourceinfo.objects.all()
    serializer_class = adminserializers.ResourceinfoSerializer
    
    def list(self, request):
        classid   = request.GET.get('classid')
        section   = request.GET.get('section')
        chapterid = request.GET.get('chapterid')
        kwarg = {}
        kwarg['isdeleted'] = 0
        if classid:
            kwarg['classid'] = classid
        if section:
            kwarg['section'] = section
        if chapterid:
            kwarg['chapterid'] = chapterid
        
        queryset = models.Resourceinfo.objects.filter(**kwarg)
        serializer = adminserializers.ResourceinfoSerializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request):
        ri = models.Resourceinfo()
        #print request.DATA, type(request.DATA)
        ridata =  json.loads(dict(request.DATA).keys()[0])
        print ridata
        category = ridata.get('categoryid')
        if category == 'text' :
            categoryid = 0
        elif category == 'audio':
            categoryid = 1
        elif category == 'video':
            category = 2
        elif category == 'image':
            category = 3


        ri.categoryid = categoryid
        ri.classid = int(ridata.get('classid'))
        ri.section = ridata.get('section')
        ri.chapterid = ridata.get('chapterid')
        ri.resourcetype = category
        ri.chapterid = ridata.get('chapterid')
        ri.resourcetitle = ridata.get('resourcetitle')
        ri.resourcedescription = ridata.get('resourcedescription', "")
        ri.thumbnailurl = ""# ridata.get('thumbnailurl', "")
        ri.documenturl = ""
        ri.imageurl = ""
        ri.audiourl = ""
        ri.videourl = ""
        if category == 'text' : 
            ri.documenturl = ridata.get('fileurl',"")
        elif category == 'image':
            ri.imageurl = ridata.get('fileurl',"")
        elif category == 'audio':    
            ri.audiourl = ridata.get('fileurl',"")
        elif category == 'video':
            ri.videourl = ridata.get('fileurl',"")
        ri.originaltext = ridata.get('originaltext',"")
        ri.createdby = request.user.id
        ri.isapproved = 0
        ri.isdeleted = 0
        ri.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        ri.save()
        return Response(request.DATA)

class WrittenworkinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Writtenworkinfo.objects.all()
    serializer_class = adminserializers.WrittenworkinfoSerializer
    
class ChapterinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Chapterinfo.objects.all()
    serializer_class = adminserializers.ChapterinfoSerializer
    
    def list(self, request):
        classid   = request.GET.get('classid')
        sectionid   = request.GET.get('section')
        chapterid = request.GET.get('chapterid')
        kwarg = {}
        #kwarg['isdeleted'] = 0
        if classid:
            kwarg['classid'] = classid
        if sectionid:
            kwarg['sectionid'] = sectionid
        if chapterid:
            kwarg['chapterid'] = chapterid
        if len(kwarg):
            queryset = models.Chapterinfo.objects.filter(**kwarg).order_by('chaptername')
        else:
            queryset = models.Chapterinfo.objects.all().order_by('chaptername')
        serializer = adminserializers.ChapterinfoSerializer(queryset, many=True)
        return Response(serializer.data)
 
class AdminclassinfoViewSet(viewsets.ModelViewSet): 
    queryset = models.Classroominfo.objects.all()
    serializer_class = adminserializers.ClassroominfoSerializer

    def list(self, request):
        sql = """
        SELECT DISTINCT 
           cri.classroomid,
           cri.assessmentid, 
           cri.resourceid,
           al.assessmenttype,
           al.assessmenttitle,
           ri.resourcetype,
           ri.resourcetitle,
           wwi.writtenworktitle,
           cri.writtenworkid, 
           si.firstname,
           si.imageurl,
           date(cri.posteddate) as posteddate,
           cri.studentid
        FROM classroominfo cri
        LEFT OUTER JOIN assignassessmentinfo aai ON aai.assessmentid = cri.assessmentid 
                        AND aai.studentid = cri.studentid 
        LEFT OUTER JOIN assessmentlist al ON al.assessmentid = cri.assessmentid 
        LEFT OUTER JOIN assignresourceinfo ari  ON ari.resourceid = cri.resourceid 
                        AND ari.studentid = cri.studentid 
        LEFT OUTER JOIN resourceinfo ri ON ri.resourceid = cri.resourceid
        LEFT OUTER JOIN assignwrittenworkinfo awwi ON awwi.writtenworkid = cri.writtenworkid
        LEFT OUTER JOIN writtenworkinfo wwi ON wwi.writtenworkid = cri.writtenworkid
        LEFT OUTER JOIN logininfo li ON li.loginid = cri.studentid
        LEFT OUTER JOIN studentinfo si ON si.username = li.username
        /*
        WHERE ( ari.isclassroom =1 OR 
                 aai.isclassroom =1 OR 
                awwi.isclassroom=1 ) 
        */
        ORDER BY cri.classroomid DESC
        """
        queryset = models.Classroominfo.objects.raw(sql)
        serializer_class = adminserializers.ClassroominfoSerializer
        serializer = adminserializers.ClassroominfoSerializer(queryset, many=True)        
        return Response({"test":"test"})

class AdminschoolViewSet(viewsets.ModelViewSet):

    queryset = models.Schoolinfo.objects.all()
    serializer_class = adminserializers.AdminschoolSerializer

    def create(self, request):
        adminschools = models.Schoolinfo()
        schooldata =  json.loads(request.DATA.keys()[0])
        adminschools.schoolname = schooldata.get('schoolname')
        adminschools.shortname = schooldata.get('shortname')
        adminschools.description = schooldata.get('description')
        adminschools.createdby = request.user.id
        adminschools.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        adminschools.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        adminschools = models.Schoolinfo.objects.get(pk=pk)
        schooldata =  json.loads(request.DATA.keys()[0])
        adminschools.schoolname = schooldata.get('schoolname')
        adminschools.shortname = schooldata.get('shortname')
        adminschools.description = schooldata.get('description')
        adminschools.createdby = request.user.id
        adminschools.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        adminschools.save()
        return Response(request.DATA)


    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class AdminclasslistViewSet(viewsets.ModelViewSet):

    queryset = models.Classinfo.objects.all()
    serializer_class = adminserializers.AdminclasslistSerializer
    def list(self,request):
        classid   = request.GET.get('classid')
        section   = request.GET.get('section')
        chapterid = request.GET.get('chapterid')
        kwarg = {}
        if classid:
            kwarg['classid'] = classid
        if section:
            kwarg['section'] = section
        if chapterid:
            kwarg['chapterid'] = chapterid
        if len(kwarg):
            queryset = models.Classinfo.objects.filter(**kwarg)
        else:
            queryset = models.Classinfo.objects.all()
        serializer = adminserializers.AdminclasslistSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        adminclasslist = models.Classinfo()
        classlistdata =  json.loads(request.DATA.keys()[0])
        adminclasslist.classname = classlistdata.get('classname')
        adminclasslist.shortname = classlistdata.get('shortname')
        adminclasslist.createdby = request.user.id
        adminclasslist.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        adminclasslist.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class AdminrubricsViewSet(viewsets.ModelViewSet):

    queryset = models.RubricsHeader.objects.all()
    serializer_class = adminserializers.AdminrubricsSerializer

    def create(self, request):
        adminrubrics = models.Rubricsheader()
        rubricsdata =  json.loads(request.DATA.keys()[0])
        adminrubrics.title = rubricsdata.get('title')
        adminrubrics.description = rubricsdata.get('description')
        adminrubrics.teacher = rubricsdata.get('teacher')
        adminrubrics.status = rubricsdata.get('status')
        adminrubrics.ts = time.strftime('%Y-%m-%d %H:%M:%S')
        adminrubrics.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class AssignresourceinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Assignresourceinfo.objects.all()
    serializer_class = adminserializers.AssignresourceinfoSerializer

    def create(self, request):
        adminassignresource = models.Assignresourceinfo()
        rubricsdata =  json.loads(request.DATA.keys()[0])
        adminrubrics.resourceid = rubricsdata.get('resourceid')
        adminrubrics.IsDelete = rubricsdata.get('IsDelete')
        adminrubrics.assignedby = rubricsdata.get('assignedby')
        adminrubrics.assigneddate = time.strftime('%Y-%m-%d %H:%M:%S')
        adminrubrics.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class WorkspaceViewSet(viewsets.ModelViewSet):

    queryset = models.Workspaceinfo.objects.all()
    serializer_class = adminserializers.WorkspaceinfoSerializer

    def create(self, request):
        adminassignresource = models.Workspaceinfo()
        rubricsdata =  json.loads(request.DATA.keys()[0])
        adminrubrics.resourceid = rubricsdata.get('resourceid')
        adminrubrics.IsDelete = rubricsdata.get('IsDelete')
        adminrubrics.assignedby = rubricsdata.get('assignedby')
        adminrubrics.assigneddate = time.strftime('%Y-%m-%d %H:%M:%S')
        adminrubrics.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = models.Calendardetails.objects.all()
    serializer_class = adminserializers.CalendarSerializer

    def create(self, request):
        cal = models.Calendardetails()
        data = json.loads(dict(request.DATA).keys()[0])
        #return Response({})
        #data = {k:v[0] for k,v in dict(request.DATA).items()}
        cal.title = data.get('title')
        cal.start = data.get('start')
        cal.end = data.get('end')
        cal.isdeleted = 0
        cal.createdby = request.user.id
        cal.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        cal.save()
        return Response(request.DATA)

class MindmapViewSet(viewsets.ModelViewSet):
    queryset = models.Mindmap.objects.all()
    serializer_class = adminserializers.MindmapSerializer

    def create(self, request):
        mm = models.Mindmap()
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        mm.title = data.get('title')
        mm.mapdata = data.get('mapdata')
        mm.isdelete = 0
        mm.createdby = 1 #request.user.id
        mm.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        mm.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        mm = models.Mindmap.objects.get(pk=pk)  
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        mm.title = data.get('title')
        mm.mapdata = data.get('mapdata')
        mm.isdelete = 0
        mm.createdby = 1 #request.user.id
        mm.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        mm.save()
        return Response(request.DATA)
        


class StudentAssignResource(viewsets.ModelViewSet):
    queryset = models.Assignresourceinfo.objects.all()
    serializer_class = adminserializers.MindmapSerializer

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        #print data
        ari = models.Assignresourceinfo.objects.get(pk=pk)
        ari.originaltext = data.get('originaltext')
        ari.answertext = data.get('answertext')
        ari.answerurl = data.get('answerurl')
        ari.isrecord = 1
        if data.get('isanswered'):
            ari.isanswered = data.get('isanswered')
            ari.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')
        if data.get('issaved'):
            ari.issaved = data.get('issaved')
        ari.save()
        return Response({'msg':True})

    def list(self, request):
        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))

        sql = '''
        SELECT assignedid AS id,
               ri.resourceid,
               resourcetitle,
               date(assigneddate) as createddate,
               resourcetype,
               thumbnailurl,
               ari.studentid,
               ari.isanswered,
               ari.issaved
        FROM assignresourceinfo ari
        INNER JOIN  resourceinfo ri on ri.resourceid = ari.resourceid 
        WHERE isdeleted=0
              AND ari.studentid=%d
              AND ari.IsDelete=0 
              AND ri.categoryid=0 
              %s
        GROUP BY resourceid 
        ORDER BY assigneddate DESC''' % (loginname_to_userid('Student', 'T0733732E'), datecond)
        cursor = connection.cursor()
        print sql
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

    def retrieve(self, request, pk=None):
        sql = '''
        SELECT assignedid AS id,
               ri.resourceid,
               ri.videourl,
               resourcetitle,
               date(assigneddate) as createddate,
               resourcetype,
               thumbnailurl,
               ari.answertext,
               ari.studentid,
               ari.isanswered,
               ari.issaved
        FROM assignresourceinfo ari
        INNER JOIN  resourceinfo ri on ri.resourceid = ari.resourceid 
        WHERE assignedid = %s
        ''' % pk
        cursor = connection.cursor()
        cursor.execute(sql)
        result = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
        print result
        return Response(result)

    def create(self, request):
        data = json.loads(dict(request.DATA).keys()[0]);
        students = data.get('students');
        resource = data.get('resource');
        rubricid = data.get('rubricid');
        assigntext = data.get('assigntext');
        print resource
        print students
        print resource, students
        for r in resource:
            for s in students:
                ar = models.Assignresourceinfo()
                ar.resourceid = int(r)
                ar.studentid = int(s)
                ar.assigntext = str(assigntext)
                ar.isanswered = 0
                ar.issaved = 0
                ar.isrecord = 0
                ar.answerrating = 0
                ar.isbillboard = 0
                ar.isclassroom = 0
                ar.answereddate = '1910-01-01'
                ar.assignedby = 1 #request.user.userid
                ar.assigneddate = time.strftime('%Y-%m-%d %H:%M:%S')
                ar.isdelete = 0
                ar.rubric_id = int(rubricid)
                ar.old_edit = 0
                ar.save()   
        
        return Response(request.DATA)


class TeacherStudentAssignResource(viewsets.ModelViewSet):
    queryset = models.Assignresourceinfo.objects.all()
    serializer_class = adminserializers.MindmapSerializer

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        #print data
        ari = models.Assignresourceinfo.objects.get(pk=pk)
        ari.originaltext = data.get('originaltext')
        ari.answertext = data.get('answertext')
        ari.answerurl = data.get('answerurl')
        ari.isrecord = 1
        if data.get('isanswered'):
            ari.isanswered = data.get('isanswered')
            ari.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')
        if data.get('issaved'):
            ari.issaved = data.get('issaved')
        ari.save()
        return Response({'msg':True})

    def list(self, request):
        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))

        sql = '''
        SELECT assignedid AS id,
               ri.resourceid,
               resourcetitle,
               date(assigneddate) as createddate,
               resourcetype,
               thumbnailurl,
               ari.studentid,
               ari.isanswered,
               ari.issaved
        FROM assignresourceinfo ari
        INNER JOIN  resourceinfo ri on ri.resourceid = ari.resourceid 
        WHERE isdeleted=0
              AND ari.assignedby=%d
              AND ari.IsDelete=0 
              AND ri.categoryid=0 
              %s
        GROUP BY resourceid 
        ORDER BY assigneddate DESC''' % (loginname_to_userid('Teacher', 'sheela'), datecond)

        #ORDER BY assigneddate DESC''' % (loginname_to_userid('Student', 'T0733732E'), datecond)
        cursor = connection.cursor()
        print sql
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

    def retrieve(self, request, pk=None):
        sql = '''
        SELECT assignedid AS id,
               ri.resourceid,
               ri.videourl,
               resourcetitle,
               date(assigneddate) as createddate,
               resourcetype,
               thumbnailurl,
               ari.answertext,
               ari.studentid,
               ari.isanswered,
               ari.issaved
        FROM assignresourceinfo ari
        INNER JOIN  resourceinfo ri on ri.resourceid = ari.resourceid 
        WHERE ari.resourceid = %s
        ''' % pk
        cursor = connection.cursor()
        cursor.execute(sql)
        result = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
        return Response(result)

    def create(self, request):
        data = json.loads(dict(request.DATA).keys()[0]);
        students = data.get('students');
        resource = data.get('resource');
        rubricid = data.get('rubricid');
        assigntext = data.get('assigntext');
        print resource
        print students
        print resource, students
        for r in resource:
            for s in students:
                ar = models.Assignresourceinfo()
                ar.resourceid = int(r)
                ar.studentid = int(s)
                ar.assigntext = str(assigntext)
                ar.isanswered = 0
                ar.issaved = 0
                ar.isrecord = 0
                ar.answerrating = 0
                ar.isbillboard = 0
                ar.isclassroom = 0
                ar.answereddate = '1910-01-01'
                ar.assignedby = 1 #request.user.userid
                ar.assigneddate = time.strftime('%Y-%m-%d %H:%M:%S')
                ar.isdelete = 0
                ar.rubric_id = int(rubricid)
                ar.old_edit = 0
                ar.save()   
        
        return Response(request.DATA)



class StickynotesResource(viewsets.ModelViewSet):
    queryset = models.stickynotes.objects.all()
    serializer_class = adminserializers.StickynotesSerializer

    def list(self, request):
        sql = '''
        SELECT s.id,
            s.stickytext,
            s.color,
            group_concat(sc.stickycomment SEPARATOR "~") as comments,
            group_concat(sc.commentby SEPARATOR "~") as commentby
        FROM stickynotes s
        LEFT JOIN stickycomments sc ON sc.stickyid = s.id
        GROUP BY s.id, 
                 s.stickytext,
                 s.color''' 
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)
    def create(self, request):
        stickynotes = models.stickynotes()
        data = json.loads(dict(request.DATA).keys()[0])
        stickynotes.stickytext = data.get('stickytext')
        stickynotes.name = data.get('name')
        stickynotes.xyz = data.get('xyz')
        stickynotes.color = data.get('color')
        stickynotes.isdeleted = 0
        stickynotes.createdby = request.user.id
        stickynotes.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        stickynotes.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        stickynotes = models.stickynotes.objects.get(pk=pk)
        data =  json.loads(request.DATA.keys()[0])
        stickynotes.stickytext = data.get('stickytext')
        stickynotes.name = data.get('name')
        stickynotes.xyz = data.get('xyz')
        stickynotes.color = data.get('color')
        stickynotes.isdeleted = 0
        stickynotes.createdby = request.user.id
        stickynotes.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        stickynotes.save()
        return Response(request.DATA)

    def destroy(self, request, pk):
        models.stickynotes.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

class StudentinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Studentinfo.objects.all()
    serializer_class = adminserializers.StudentinfoSerializer

    def create(self, request):
        studentinfo = models.studentinfo()
        studentdata =  json.loads(request.DATA.keys()[0])
        studentinfo.studentid = rubricsdata.get('studentid')
        studentinfo.firstname = rubricsdata.get('firstname')
        studentinfo.lastname = rubricsdata.get('lastname')
        studentinfo.username = rubricsdata.get('username')
        studentinfo.emailid = rubricsdata.get('emailid')
        studentinfo.schoolid = rubricsdata.get('schoolid')
        studentinfo.classid = rubricsdata.get('classid')
        studentinfo.password = rubricsdata.get('password')
        studentinfo.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        studentinfo.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')


class StickyCommentsResource(viewsets.ModelViewSet):
    queryset = models.stickycomments.objects.all()
    serializer_class = adminserializers.StickyCommentsSerializer

    def create(self, request):
        stickycomments = models.stickycomments()
        data = json.loads(dict(request.DATA).keys()[0])
        stickycomments.stickyid = data.get('stickyid')
        stickycomments.stickycomment = data.get('stickycomment')
        stickycomments.commentby = request.user.username
        stickycomments.isdeleted = 0
        stickycomments.createdby = request.user.id
        stickycomments.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        stickycomments.save()
        return Response(request.DATA)


class AssignedResourceStudents(viewsets.ModelViewSet):
    queryset = models.Assignresourceinfo.objects.all()
    serializer_class = adminserializers.MindmapSerializer

    def retrieve(self, request, pk=None):

        sql = '''
        SELECT assignedid AS id,
               ari.assignedby,
               ri.resourceid,
               si.firstname,
               si.lastname,
               resourcetitle,
               date(assigneddate) as createddate,
               resourcetype,
               thumbnailurl,
               ari.answereddate,
               ari.answertext,
               ari.originaltext,
               ari.studentid,
               ari.isanswered,
               ari.issaved
        FROM assignresourceinfo ari
        INNER JOIN  resourceinfo ri on ri.resourceid = ari.resourceid 
        INNER JOIN  studentinfo si on si.studentid = ari.studentid 
        WHERE isdeleted=0
              AND ari.assignedby=%d
              AND ari.resourceid=%s
              AND ari.IsDelete=0 
              AND ri.categoryid=0
        GROUP BY ari.studentid
        ORDER BY assigneddate DESC''' % (loginname_to_userid('Teacher', 'sheela'), pk)

        #ORDER BY assigneddate DESC''' % (loginname_to_userid('Student', 'T0733732E'), datecond)
        cursor = connection.cursor()
        print sql
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


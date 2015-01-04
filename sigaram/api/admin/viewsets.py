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

    queryset = models.Admininfo.objects.filter(isdelete=0).order_by('-createddate')
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
        classid  =  request.GET.get('classid')

        if schoolid and classid:
            queryset = models.Teacherinfo.objects.filter(schoolid=schoolid, classid=classid).order_by('-createddate')
        elif schoolid:
            queryset = models.Teacherinfo.objects.filter(schoolid=schoolid).order_by('-createddate')
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
        teacher.classid = teacherdata.get('classid')
        teacher.emailid = teacherdata.get('emailid')
        teacher.imageurl = teacherdata.get('imageurl')
       # teacher.imageurl = #studentdata.get('imageurl')
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
        teacher.classid = teacherdata.get('classid')
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
            queryset = models.Studentinfo.objects.filter(schoolid=schoolid, classid=classid).order_by('-createddate')
        elif schoolid:
            queryset = models.Studentinfo.objects.filter(schoolid=schoolid).order_by('-createddate')
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
    queryset = models.Teacherresourceinfo.objects.filter().order_by('-createddate')
    serializer_class = adminserializers.TeacherresourceinfoSerializer

    def list(self, request):
        sql = """
        SELECT  tri.teacherresourceid,
                tri.classid,
                tri.section,
                tri.resourcetype,
                tri.resourcetitle,
                ci.shortname,
                tri.createddate
        FROM teacherresourceinfo tri
        INNER JOIN classinfo ci ON ci.classid = tri.classid
        ORDER BY tri.createddate DESC
        """
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [dict(zip([col[0] for col in desc], row))for row in cursor.fetchall()]
        return Response(result)

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
        
        queryset = models.Resourceinfo.objects.filter(**kwarg).order_by('-createddate')
        serializer = adminserializers.ResourceinfoSerializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request):
        ri = models.Resourceinfo()
        #print request.DATA, type(request.DATA)
        ridata =  json.loads(dict(request.DATA).keys()[0])
        #print ridata
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
        ri.thumbnailurl = ridata.get('thumbnailurl', "")
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
        categoryid = request.GET.get('categoryid',0)
        
        kwarg = {}
        #kwarg['isdeleted'] = 0
        if classid:
            kwarg['classid'] = classid
        if sectionid:
            kwarg['sectionid'] = sectionid
        if chapterid:
            kwarg['chapterid'] = chapterid

        if len(kwarg):
            queryset = models.Chapterinfo.objects.filter(**kwarg).order_by('chapterid')
        else:
            queryset = models.Chapterinfo.objects.all().order_by('chapterid')

        serializer = adminserializers.ChapterinfoSerializer(queryset, many=True)
        if categoryid:
            sql = '''
            SELECT chapterid, 
                   count(*) AS cnt
            FROM resourceinfo 
            WHERE categoryid=%s
                AND classid=%s
                AND section='%s' 
            GROUP BY chapterid'''%(categoryid, classid, sectionid)
            cursor = connection.cursor()
            cursor.execute(sql)
            cnt = cursor.fetchall()
            print serializer.data
            for i, d in enumerate(serializer.data):
                for c in cnt:
                    if serializer.data[i]['chapterid'] == c[0]:
                        serializer.data[i]['rescount'] = c[1]
                        break
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

    queryset = models.Schoolinfo.objects.all().order_by('-createddate')
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
        assignresourceinfo = models.Assignresourceinfo()
        assigndata =  json.loads(request.DATA.keys()[0])
        assignresourceinfo.resourceid = assigndata.get('resourceid')
        assignresourceinfo.isdelete = 0 #assigndata.get('IsDelete')
        assignresourceinfo.assignedby = assigndata.get('assignedby')
        assignresourceinfo.assigneddate = time.strftime('%Y-%m-%d %H:%M:%S')
        assignresourceinfo.save()
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
        cal.eventcreatedby = request.user.username
        cal.eventeditedby = request.user.username
        cal.isdeleted = 0
        cal.createdby = request.user.id
        cal.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        cal.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        cal = models.Calendardetails.objects.get(pk=pk)  
        data = json.loads(dict(request.DATA).keys()[0])
        #data = {k:v[0] for k,v in dict(request.DATA).items()}
        cal.title = data.get('title')
        cal.start = data.get('start')
        cal.end = data.get('end')
        #cal.eventcreatedby = request.user.username
        #cal.start = time.strftime('%Y-%m-%d %H:%M:%S')
        #cal.end = time.strftime('%Y-%m-%d %H:%M:%S')
        cal.eventcreatedby = request.user.username
        cal.eventeditedby = request.user.username
        cal.isdeleted = 0
        cal.createdby = request.user.id
        cal.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        cal.save()
        return Response(request.DATA)

class MindmapViewSet(viewsets.ModelViewSet):
    queryset = models.Mindmap.objects.filter().order_by('-createddate')
    serializer_class = adminserializers.MindmapSerializer

    def create(self, request):
        mm = models.Mindmap()
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        mm.title = data.get('title')
        mm.mapdata = data.get('mapdata')
        mm.isdelete = 0
        mm.createdby = request.user.id
        mm.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        mm.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        mm = models.Mindmap.objects.get(pk=pk)  
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        mm.title = data.get('title')
        mm.mapdata = data.get('mapdata')
        mm.isdelete = 0
        mm.createdby = request.user.id
        mm.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        mm.save()
        return Response(request.DATA)
        


class StudentAssignResource(viewsets.ModelViewSet):
    queryset = models.Assignresourceinfo.objects.all()
    serializer_class = adminserializers.MindmapSerializer

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        
        ari = models.Assignresourceinfo.objects.get(pk=pk)
        
        ari.answertext = data.get('answertext')

        if data.get('originaltext'):
            ari.originaltext = data.get('originaltext')

        if data.get('answerurl'):
            ari.answerurl = data.get('answerurl')
            ari.isrecord = 1

        if data.get('isanswered'):
            ari.isanswered = data.get('isanswered')
            ari.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')

        if data.get('issaved'):
            ari.issaved = data.get('issaved')
        
        ari.save()

        assignedid  = pk;
        spanid      = data.get('spanid');
        fulltext    = data.get('fulltext');
        orig        = data.get('orig');
        modified    = data.get('modified');
        usertype    = data.get('type');
        answertext  = data.get('answertext');

        ar = models.Editingtext()
        ar.editid       = int(assignedid)
        ar.spanid       = str(spanid)
        ar.previoustext = str(orig)
        ar.edittext     = str(modified)
        ar.typeofresource = 0
        ar.isapproved   = 0
        ar.isrejected   = 0
        ar.editedby     = request.user.username
        ar.editeddate   = time.strftime('%Y-%m-%d %H:%M:%S')
        ar.usertype     = int(usertype)

        ar.save()

        return Response({'msg':True})

    def list(self, request):

        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))
        sql = '''
        SELECT assignedid AS id,
               ari.isrecord,
               ari.audiourl,
               ri.resourceid,
               resourcetitle,
               date(assigneddate) as createddate,
               date(answereddate) as answereddate,
               resourcetype,
               thumbnailurl,
               ari.studentid,
               ari.isanswered,
               ari.issaved
        FROM assignresourceinfo ari
        INNER JOIN  resourceinfo ri on ri.resourceid = ari.resourceid 
        WHERE isdeleted=0
              AND ari.studentid='%s'
              AND ari.IsDelete=0
              /*AND ri.categoryid=0*/
              %s
        GROUP BY resourceid 
        ORDER BY answereddate DESC''' % (request.user.username, datecond)
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
               ari.isrecord,
               ari.answerurl,
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
        #print result
        return Response(result)

    def create(self, request):
        data = json.loads(dict(request.DATA).keys()[0]);
        students = data.get('students');
        resource = data.get('resource');
        rubricid = data.get('rubricid');
        assigntext = data.get('assigntext');
       # print resource
        #print students
       # print resource, students
        for r in resource:
            for s in students:
                ar = models.Assignresourceinfo()
                ar.resourceid = int(r)
                ar.studentid = str(s)
                ar.assigntext = str(assigntext)
                ar.isanswered = 0
                ar.issaved = 0
                ar.isrecord = 0
                ar.answerrating = 0
                ar.isbillboard = 0
                ar.isclassroom = 0
                ar.answereddate = '1910-01-01'
                ar.assignedby = request.user.username
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
              AND ari.assignedby='%s'
              AND ari.IsDelete=0 
              /*AND ri.categoryid=0 */
              %s
        GROUP BY resourceid 
        ORDER BY assigneddate DESC''' % (request.user.username, datecond)

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
        #print resource
        #print students
        #print resource, students
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
            group_concat(sc.commentby SEPARATOR "~") as commentby,
            group_concat(sc.createddate SEPARATOR "~") as createddate
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
        studentcond = ''
        if request.GET.get('studentid'):
            studentcond = "AND ari.studentid = '" + request.GET.get('studentid') + "'"

        sql = '''
        SELECT assignedid AS id,
               ari.assignedby,
               ri.resourceid,
               au.first_name as firstname,
               au.last_name as lastname,
               resourcetitle,
               date(assigneddate) as createddate,
               resourcetype,
               thumbnailurl,
               date(ari.answereddate) as answereddate,
               ari.answertext,
               ari.originaltext,
               ari.studentid,
               ari.isanswered,
               ari.issaved,
               ari.isbillboard
        FROM assignresourceinfo ari
        INNER JOIN  resourceinfo ri on ri.resourceid = ari.resourceid 
        INNER JOIN  auth_user au on au.username = ari.studentid 
        WHERE isdeleted=0
              AND ari.resourceid=%s
              AND ari.IsDelete=0 
              /*AND ri.categoryid=0*/
              %s
        GROUP BY ari.studentid
        ORDER BY assigneddate DESC''' % (pk, studentcond)

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

class Bulletinboardlist(viewsets.ModelViewSet):
    queryset = models.Bulletinboardinfo.objects.all()
    serializer_class = adminserializers.BulletinboardlistinfoSerializer

    def list(self, request):
        sql = """
        SELECT  bi.bulletinboardid, 
                bi.messagetitle,
                bi.message,
                li.firstname AS postedby, 
                DATE(bi.posteddate ) AS posteddate, 
                ti.imageurl 
        FROM bulletinboardinfo bi
        INNER JOIN bulletinmappinginfo bmi ON bmi.bulletinboardid = bi.bulletinboardid
        INNER JOIN logininfo li ON li.loginid = bi.postedby 
        INNER JOIN teacherinfo ti ON ti.username = li.username 
        WHERE (viewtype =0 ) OR (viewtype =2) 
        -- AND bmi.adminid ='3866'
        GROUP BY bmi.bulletinboardid 
        """
        cursor = connection.cursor()
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
        print bbi.bulletinboardid
        #saving annoument target
        # for rl in data.get('resourcelist'):
        #     bmi = models.Bulletinmappinginfo()
        #     bmi.bulletinboardid = bbiid
        #     if data.get('cattype') == 'admin':
        #         bmi.adminid = rl
        #         bmi.viewtype = 0
        #     else:
        #         bmi.adminid = 0
        #     if data.get('cattype') == 'teacher':
        #         bmi.teacherid = rl
        #         bmi.viewtype = 2
        #     else:
        #         bmi.teacherid = 0
        #     if data.get('cattype') == 'schools':
        #         bmi.schoolid = data.get('schoolid')
        #         bmi.classid = rl
        #         bmi.viewtype = 2
        #     else:
        #         bmi.schoolid = 0
        #         bmi.classid = 0
        #     bmi.save()
        return Response(request.DATA)


class BillboardViewSet(viewsets.ModelViewSet):
    queryset = models.Billboardinfo.objects.all()
    serializer_class = adminserializers.BillboardSerializer

    def list(self, request):
        sql = """
        SELECT distinct bbi.assessmentid, 
                bbri.rating,
                bbi.resourceid,
                asl.assessmenttype,
                asl.assessmenttitle,
                ri.resourcetype,
                ri.resourcetitle,
                writtenworkinfo.writtenworktitle,
                bbi.writtenworkid, 
                studentinfo.firstname,
                studentinfo.imageurl,
                date(bbi.posteddate) as posteddate,
                bbi.studentid 
        FROM billboardinfo bbi
        LEFT OUTER JOIN assignassessmentinfo asm ON asm.assessmentid = bbi.assessmentid 
            AND asm.studentid = bbi.studentid 
        LEFT OUTER JOIN assessmentlist asl ON asl.assessmentid = bbi.assessmentid 
        LEFT OUTER JOIN billboardratinginfo bbri ON bbri.billboardid = bbi.billboardid 
        LEFT OUTER JOIN assignresourceinfo ari ON ari.resourceid = bbi.resourceid 
            AND ari.studentid = bbi.studentid 
        LEFT OUTER JOIN resourceinfo ri ON ri.resourceid = bbi.resourceid
        LEFT OUTER JOIN assignwrittenworkinfo awi on awi.writtenworkid = bbi.writtenworkid
        LEFT OUTER JOIN writtenworkinfo on writtenworkinfo.writtenworkid = bbi.writtenworkid
        LEFT OUTER JOIN logininfo on logininfo.loginid = bbi.studentid
        LEFT OUTER JOIN studentinfo on studentinfo.username=logininfo.username
        WHERE ( ari.isbillboard =1 OR asm.isbillboard =1 OR awi.isbillboard=1 ) 
        ORDER BY bbi.billboardid desc  """ 

        cursor = connection.cursor()
        print sql
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

    def create(self, request):
        billboard = models.Billboardinfo()
        billboarddata =  json.loads(request.DATA.keys()[0])
        billboard.billboardid = billboarddata.get('billboardid')
        billboard.assessmentid = billboarddata.get('assessmentid')
        billboard.resourceid = billboarddata.get('resourceid')
        billboard.writtenworkid = billboarddata.get('writtenworkid',0)
        billboard.studentid = billboarddata.get('studentid',0)
        billboard.votescount = billboarddata.get('votescount',0)
        billboard.lastvotedby = billboarddata.get('lastvotedby',0)
        billboard.postedby = billboarddata.get('postedby',0)
        billboard.lastvoteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        billboard.posteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        billboard.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')


class Bulletinboard(viewsets.ModelViewSet):
    queryset = models.Classschoolmappinginfo.objects.all()
    serializer_class = adminserializers.BulletinboardSerializer
    
    def list(self, request):
        schoolid =  request.GET.get('schoolid')
        if schoolid:
            wherecond = "WHERE csmi.schoolid=%s" % schoolid
        else:
            wherecond = ""
        sql = """
        SELECT  ci.shortname,
                si.shortname AS schoolname,
                csmi.classschoolmappingid AS classid 
        FROM classschoolmappinginfo csmi
        INNER JOIN classinfo ci ON ci.classid = csmi.classid 
        INNER JOIN schoolinfo si ON si.schoolid = csmi.schoolid 
        %s 
        ORDER BY ci.classid """ % wherecond;
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

    def create(self, request):
        announcement = models.Bulletinboardinfo()
        data = json.loads(dict(request.DATA).keys()[0])
        announcement.messagetitle = data.get('messagetitle')
        announcement.message = data.get('message')
        announcement.schoolid = data.get('schoolid',0)
        announcement.classid = data.get('classid',0)
        announcement.postedby = request.user.id
        announcement.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        announcement.save()
        return Response(request.DATA)

class Bulletinmappinginfo(viewsets.ModelViewSet):
    queryset = models.Bulletinmappinginfo.objects.all()
    serializer_class = adminserializers.BulletinmappinginfoSerializer
    
    def create(self, request):
        bulletmapping = models.Bulletinmappinginfo()
        data = json.loads(dict(request.DATA).keys()[0])
        resource = data.get('resource',[]);
        cattype = data.get('cattype');
        if cattype == 'admin':
            for ai in resource:
               # bulletmapping.bulletinboardid = data.get('bulletinboardid')
                bulletmapping.viewtype = data.get('viewtype',0)
                bulletmapping.schoolid = 0 # data.get('schoolid')
                bulletmapping.classid = 0 #data.get('classid')
                bulletmapping.adminid = ai #data.get('adminid')
                bulletmapping.teacherid = 0 #data.get('teacherid')
                bulletmapping.save()
        elif cattype == 'teacher':
            for ti in resource:
                #bulletmapping.bulletinboardid = data.get('bulletinboardid')
                bulletmapping.viewtype = data.get('viewtype',0)
                bulletmapping.schoolid = 0 #data.get('schoolid')
                bulletmapping.classid = 0 #data.get('classid')
                bulletmapping.adminid = 0 #data.get('adminid')
                bulletmapping.teacherid = ti #data.get('teacherid')
                bulletmapping.save()
        else:
            for ci in resource:
                #bulletmapping.bulletinboardid = data.get('bulletinboardid')
                bulletmapping.viewtype = data.get('viewtype',0)
                bulletmapping.schoolid = data.get('schoolid')
                bulletmapping.classid = ci
                bulletmapping.adminid = 0 #data.get('adminid')
                bulletmapping.teacherid = 0 #data.get('teacherid')
                bulletmapping.save()

        return Response(request.DATA)

class EditAnswerViewSet(viewsets.ModelViewSet):
    queryset = models.Editingtext.objects.all()
    serializer_class = adminserializers.EditingtextSerializer

    def list(self, request):

        spanid = request.GET.get('spanid')
        assignedid = request.GET.get('assignedid')

        sql = """
        SELECT editingid, 
               editid, 
               spanid, 
               previoustext, 
               edittext, 
               CONCAT(au.first_name,' ',au.last_name ) AS name,
               editeddate AS edate,
               isapproved,
               et.usertype
        FROM  editingtext et
        INNER JOIN auth_user au 
            ON au.username = et.editedby
        WHERE  et.editid = '%s'
            AND et.spanid = '%s'
        ORDER BY editeddate desc """ % (assignedid,spanid)

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

    def retrieve(self, request, pk=None):
        assignedid = request.GET.get('assignedid')
        previoustext = request.GET.get('previoustext')
        sql = '''
        SELECT et.previoustext,
            et.edittext,
            ari.answertext,
            et.spanid
        FROM editingtext et
        JOIN assignresourceinfo ari 
            ON ari.assignedid = et.editid   
        WHERE et.editingid = %s''' % (pk)
        cursor = connection.cursor()
        cursor.execute(sql)
        rec =  cursor.fetchone()
        previoustext = rec[0]
        edittext = rec[1]
        answertext = rec[2]
        spanid = rec[3]

        # print edittext
        # print previoustext
        # print answertext

        approvedanswertext = answertext.replace(previoustext,edittext)

        #updating approved answer text
        sql = '''
        UPDATE assignresourceinfo 
           SET answertext = "%s"
           WHERE assignedid = '%s' ''' % (str(approvedanswertext), assignedid)
        cursor = connection.cursor()
        cursor.execute(sql)

        #resetting the previous one if set
        sql = '''
        UPDATE editingtext
            SET isapproved = 0
        WHERE spanid = '%s' ''' % (spanid)
        cursor = connection.cursor()
        cursor.execute(sql)

        # #marking the selected as approved
        sql = '''
        UPDATE editingtext
            SET isapproved = 1,
            previoustext = "%s"
        WHERE editingid = '%s' ''' % (edittext, pk)
        cursor = connection.cursor()
        cursor.execute(sql)

        return Response('approved')

    def create(self, request):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        
        assignedid  = data.get('assignedid');
        spanid      = data.get('spanid');
        prevtext    = data.get('prevtext');
        modified    = data.get('modified');
        usertype    = data.get('type');

        et = models.Editingtext()
        et.editid       = int(assignedid)
        et.spanid       = str(spanid)
        et.previoustext = str(prevtext)
        et.edittext     = str(modified)
        et.typeofresource = 0
        et.isapproved   = 0
        et.isrejected   = 0
        et.editedby     = request.user.username
        et.editeddate   = time.strftime('%Y-%m-%d %H:%M:%S')
        et.usertype     = str(usertype)

        et.save()

        return Response('"msg":"Approved successfully"')


class BillboardResourceViewSet(viewsets.ModelViewSet):
    queryset = models.Billboardinfo.objects.all()
    serializer_class = adminserializers.BillboardSerializer

    def create(self, request):
        billboard = models.Billboardinfo()
        studentid  = request.GET.get('studentid');
        resourceid = request.GET.get('resourceid');
        billboard.assessmentid = 0
        billboard.resourceid = resourceid
        billboard.writtenworkid = 0
        billboard.studentid = str(studentid)
        billboard.votescount = 0
        billboard.lastvotedby = 0
        billboard.postedby = str(request.user.username)
        billboard.posteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        billboard.save()

        sql = '''
        UPDATE assignresourceinfo
            SET isbillboard = 1
        WHERE studentid = '%s'
            AND resourceid = '%s' ''' % (str(studentid), resourceid)

        cursor = connection.cursor()
        cursor.execute(sql)        

        return Response('saved')

class TopicViewSet(viewsets.ModelViewSet):

    queryset = models.Topicinfo.objects .all()
    serializer_class = adminserializers.TopicsSerializer

    def create(self, request):
        topics = models.Topicinfo()
        topicinfodata =  json.loads(request.DATA.keys()[0])
        topics.topicid = topicinfodata.get('topicid',0)
        topics.forumid = topicinfodata.get('forumid',0)
        topics.topicname = topicinfodata.get('topicname',0)
        topics.createdby = request.user.id
        topics.lastpostedby = request.user.id
        topics.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
import json, time
from api.admin import (create_login, 
                       delete_login)

from portaladmin import models
import  adminserializers

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
        #teacher.imageurl = studentdata.get('imageurl')
        teacher.isdelete = 0
        teacher.createdby = request.user.id
        teacher.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        teacher.save()
        return Response(request.DATA)

class studentViewSet(viewsets.ModelViewSet):
    queryset = models.Studentinfo.objects.filter(isdelete=0)
    serializer_class = adminserializers.StudentinfoSerializer
    
    def list(self, request):
        schoolid =  request.GET.get('schoolid')
        classid  =  request.GET.get('classid')

        if schoolid and classid:
            queryset = models.Studentinfo.objects.filter(schoolid=schoolid, classid=classid)
        elif schoolid:
            queryset = models.Studentinfo.objects.filter(schoolid=schoolid)
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
        #student.imageurl = studentdata.get('imageurl')
        student.isdelete = 0
        student.createdby = request.user.id
        student.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        student.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response(pk)

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
        teacherresource.schoolid = teacherresourcedata.get('schoolid')
        teacherresource.classid = teacherresourcedata.get('classid')
        teacherresource.section = teacherresourcedata.get('section')
        teacherresource.resourcetype = teacherresourcedata.get('resourcetype')
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
        ridata =  json.loads(request.DATA.keys()[0])
        
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
        ri.originaltext = "" #ridata.get('originaltext')
        ri.resourcetitle = "" #ridata.get('resourcetitle')
        ri.resourcedescription = "" #ridata.get('resourcedescription')
        ri.thumbnailurl =  "" #ridata.get('thumbnailurl')
        ri.documenturl = ""
        ri.imageurl = ""
        ri.audiourl = ""
        ri.videourl = ""
        if category == 'text' : 
            ri.documenturl = ridata.get('documenturl')
        elif category == 'image':
            ri.imageurl = ridata.get('documenturl')
        elif category == 'audio':    
            ri.audiourl = ridata.get('documenturl')
        elif category == 'video':
            ri.videourl = ridata.get('documenturl')
        ri.createdby = ridata.get('createdby')
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
            queryset = models.Chapterinfo.objects.filter(**kwarg)
        else:
            queryset = models.Chapterinfo.objects.all()
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
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class AdminclasslistViewSet(viewsets.ModelViewSet):

    queryset = models.Classinfo.objects.all()
    serializer_class = adminserializers.AdminclasslistSerializer

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
        data = {k:v[0] for k,v in dict(request.DATA).items()}
        cal.title = data.get('title')
        cal.start = data.get('start')
        cal.end = data.get('end')
        cal.isdeleted = 0
        cal.createdby = request.user.id
        cal.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        cal.save()
        return Response(request.DATA)

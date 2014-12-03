from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
import json, time
from api.admin import create_login

from portaladmin import models
import  adminserializers

class AdmininfoViewSet(viewsets.ModelViewSet):

    queryset = models.Admininfo.objects.filter(isdelete=0)
    serializer_class = adminserializers.AdminInfoSerializer

    @create_login
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

    def destroy(self, request, pk=None):
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
        adminclasslist.classname = adminclasslist.get('classname')
        adminclasslist.shortname = adminclasslist.get('shortname')
        adminclasslist.createdby = request.user.id
        adminclasslist.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        adminclasslist.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')
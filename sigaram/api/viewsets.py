from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers

from portaladmin import models
import  adminserializers

class AdmininfoViewSet(viewsets.ModelViewSet):

    queryset = models.Admininfo.objects.all()
    serializer_class = adminserializers.AdminInfoSerializer

    def list(self, request):
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
        queryset = models.Admininfo.objects.raw(sql)
        serializer = adminserializers.AdminInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        return Response('"msg":"Created Successfully"')

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
    queryset = models.Studentinfo.objects.all()
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
    '''
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
    '''
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
        SELECT -- DISTINCT 
           cri.classroomid,
           cri.assessmentid, 
           cri.resourceid,
           -- al.assessmenttype,
           -- al.assessmenttitle,
           ri.resourcetype,
           ri.resourcetitle,
           -- wwi.writtenworktitle,
           cri.writtenworkid, 
           -- si.firstname,
           -- si.imageurl,
           date(cri.posteddate) as posteddate,
           cri.studentid
        FROM classroominfo cri
        -- LEFT OUTER JOIN assignassessmentinfo aai ON aai.assessmentid = cri.assessmentid 
        --                AND aai.studentid = cri.studentid 
        -- LEFT OUTER JOIN assessmentlist al ON al.assessmentid = cri.assessmentid 
        -- LEFT OUTER JOIN assignresourceinfo ari  ON ari.resourceid = cri.resourceid 
        --                AND ari.studentid = cri.studentid 
        LEFT OUTER JOIN resourceinfo ri ON ri.resourceid = cri.resourceid
        -- LEFT OUTER JOIN assignwrittenworkinfo awwi ON awwi.writtenworkid = cri.writtenworkid
        -- LEFT OUTER JOIN writtenworkinfo wwi ON wwi.writtenworkid = cri.writtenworkid
        -- LEFT OUTER JOIN logininfo li ON li.loginid = cri.studentid
        -- LEFT OUTER JOIN studentinfo si ON si.username = li.username
        -- WHERE ( ari.isclassroom =1 OR 
        --         aai.isclassroom =1 OR 
        --        awwi.isclassroom=1 ) 
        ORDER BY cri.classroomid DESC
        """
        queryset = models.Classroominfo.objects.raw(sql)
        serializer_class = adminserializers.ClassroominfoSerializer
        serializer = adminserializers.ClassroominfoSerializer(queryset, many=True)        
        return Response(serializer.data)
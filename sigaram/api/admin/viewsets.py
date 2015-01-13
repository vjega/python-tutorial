from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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

    def create(self, request):
        adminfolder = models.AdminFolders()
        data =  json.loads(request.DATA.keys()[0])
        adminfolder.folder_name = data.get('folder_name')
        adminfolder.folder_description = data.get('remark')
        adminfolder.folder_order = data.get('order_no')
        adminfolder.added_date = time.strftime('%Y-%m-%d %H:%M:%S')
        adminfolder.userid = request.user.username
        adminfolder.save()
        return Response(request.DATA)

    def destroy(self, request, pk):
        models.AdminFolders.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = models.Teacherinfo.objects.all()
    serializer_class = adminserializers.TeacherinfoSerializer
    def list(self, request):

        schoolid =  request.GET.get('schoolid')
        classid  =  request.GET.get('classid')
        username = request.GET.get('username')
       
        if schoolid and classid and username:
            queryset = models.Teacherinfo.objects.filter(schoolid=schoolid, classid=classid).order_by('-createddate')
        elif schoolid:
            queryset = models.Teacherinfo.objects.filter(schoolid=schoolid).order_by('-createddate')
        elif username:
            queryset = models.Teacherinfo.objects.filter(username=username)

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
        print "Hi"
        """
        print request.DATA
        teacher = models.Teacherinfo.objects.get(pk=pk)
        teacherdata =  json.loads(request.DATA.keys()[0])
        teacher.username = teacherdata.get('username')
        teacher.lastname = teacherdata.get('lastname')
        teacher.password = teacherdata.get('password')
        teacher.firstname = teacherdata.get('firstname')
        teacher.schoolid = teacherdata.get('schoolid')
        teacher.imageurl = teacherdata.get('imageurl')
        teacher.classid = teacherdata.get('classid')
        teacher.emailid = teacherdata.get('emailid')
        teacher.save()
        """
        return Response(request.DATA)

    def partial_update(self, request, pk=None):
        print "Hi"
        pass

    def retrieve(self, request, pk=None):
        queryset = models.Teacherinfo.objects.filter(username=request.user.username)[0]
        serializer = adminserializers.TeacherinfoSerializer(queryset, many=False)
        return Response(serializer.data)
        

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
        # schoolid   = request.GET.get('schoolid')
        # classid   = request.GET.get('classid')
        # section   = request.GET.get('section')
        # chapterid = request.GET.get('chapterid')
        # categoryid = request.GET.get('resourcecategory')

        schoolid    = ''
        classid     = ''
        section     = ''
        chapterid   = ''
        categoryid  = ''

        if request.GET.get('schoolid'):
            schoolid = "AND tri.schoolid='%s'" % (request.GET.get('schoolid'))
        if request.GET.get('classid'):
            classid = "AND tri.classid='%s'" % (request.GET.get('classid'))
        if request.GET.get('section'):
            section = "AND tri.section='%s'" % (request.GET.get('section'))
        if request.GET.get('chapterid'):
            chapterid = "AND tri.chapterid='%s'" % (request.GET.get('chapterid'))
        if request.GET.get('resourcecategory'):
            categoryid = "AND tri.resourcecategory='%s'" % (request.GET.get('resourcecategory'))


        sql = """
        SELECT  tri.teacherresourceid,
                tri.resourcetitle,
                tri.createddate,
                ci.shortname as levelname,
                tri.resourcetype
        FROM teacherresourceinfo tri
        INNER JOIN classinfo ci ON ci.classid=tri.classid
        WHERE isdeleted=0
        %s 
        %s 
        %s 
        %s 
        %s
        ORDER BY tri.createddate DESC
        """ % (schoolid,classid,section,chapterid,categoryid)
        cursor = connection.cursor()
        # print sql

        cursor.execute(sql)
        desc = cursor.description
        result =  [dict(zip([col[0] for col in desc], row))for row in cursor.fetchall()]
        return Response(result)

    def create(self, request):
        teacherresource = models.Teacherresourceinfo()
        teacherresourcedata =  json.loads(request.DATA.keys()[0])
        restype = teacherresourcedata.get('resourcetype')
        teacherresource.schoolid = teacherresourcedata.get('schoolid')
        teacherresource.classid = teacherresourcedata.get('classid',0)
        teacherresource.section = teacherresourcedata.get('section',0)
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
        teacherresource.chapterid = teacherresourcedata.get('chapterid',0)
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
        categoryid = request.GET.get('categoryid')
        resourceid = request.GET.get('resourceid')
        kwarg = {}
        kwarg['isdeleted'] = 0
        if classid:
            kwarg['classid'] = classid
        if section:
            kwarg['section'] = section
        if chapterid:
            kwarg['chapterid'] = chapterid
        if categoryid:
            kwarg['categoryid'] = categoryid

        queryset = models.Resourceinfo.objects.filter(**kwarg).order_by('resourceid')
        serializer = adminserializers.ResourceinfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = models.Resourceinfo.objects.get(pk=pk)
        serializer = adminserializers.ResourceinfoSerializer(queryset, many=False)
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
        ri.resourceid = ridata.get('resourceid')
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

    def list(self, request):
        queryset = models.Writtenworkinfo.objects.filter(createdby=str(request.user.username)).order_by('-createddate')
        serializer = adminserializers.WrittenworkinfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        models.Writtenworkinfo.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

    def retrieve(self, request, pk=None):
        sql = '''
        SELECT assignwrittenworkid AS id,
               wwi.writtenworkid,
               wwi.writtenImage,
               wwi.writtenworktitle,
               date(wwi.createddate) as createddate,
               awwi.studentid,
               wwi.isassigned,
               awwi.issaved
        FROM assignwrittenworkinfo awwi
        INNER JOIN writtenworkinfo wwi on wwi.writtenworkid = awwi.writtenworkid 
        WHERE awwi.writtenworkid = %s
        ''' % pk
        cursor = connection.cursor()
        cursor.execute(sql)
        result = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
        return Response(result)

    def create(self, request):    
        data = json.loads(dict(request.DATA).keys()[0]);
        students = data.get('students');
        title = data.get('title')
        note = data.get('note');
        schoolid = request.session.get('schoolid')
        classid = request.session.get('classid')
        attachmenturl = data.get('attachmenturl')

        writtenwork = models.Writtenworkinfo()
        writtenwork.writtenworktitle= title
        writtenwork.description     = note
        writtenwork.writtenimage    = attachmenturl
        writtenwork.schoolid        = schoolid
        writtenwork.classid         = classid
        writtenwork.isassigned      = 0
        writtenwork.isdeleted       = 0
        writtenwork.createdby       = str(request.user.username)
        writtenwork.createddate     = time.strftime('%Y-%m-%d %H:%M:%S')
        writtenwork.save()

        writtenworkid = writtenwork.writtenworkid

        for s in students:
            awwi = models.Assignwrittenworkinfo()
            awwi.writtenworkid = writtenworkid
            awwi.studentid = str(s)
            awwi.assigntext = str(note)
            awwi.issaved = 0
            awwi.ispublished = 0
            awwi.isrecord = 0
            awwi.answerrating = 0
            awwi.isbillboard = 0
            awwi.isclassroom = 0
            awwi.assignedby = str(request.user.username)
            awwi.assigneddate = '2015-01-01 00:00:00'
            awwi.publisheddate = '2015-01-01 00:00:00' #time.strftime('%Y-%m-%d %H:%M:%S')
            awwi.save()
        
        return Response(request.DATA)

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
            # print serializer.data
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
           -- al.assessmenttype,
           -- al.assessmenttitle,
           -- ri.resourcetype,
           -- ri.resourcetitle,
           -- wwi.writtenworktitle,
           cri.writtenworkid, 
           -- si.firstname,
           -- si.imageurl,
           date(cri.posteddate) as posteddate,
           cri.studentid
        FROM classroominfo cri
        /*
        -- LEFT OUTER JOIN assignassessmentinfo aai ON aai.assessmentid = cri.assessmentid 
                        -- AND aai.studentid = cri.studentid 
        -- LEFT OUTER JOIN assessmentlist al ON al.assessmentid = cri.assessmentid 
        -- LEFT OUTER JOIN assignresourceinfo ari  ON ari.resourceid = cri.resourceid 
                        -- AND ari.studentid = cri.studentid 
        -- LEFT OUTER JOIN resourceinfo ri ON ri.resourceid = cri.resourceid
        -- LEFT OUTER JOIN assignwrittenworkinfo awwi ON awwi.writtenworkid = cri.writtenworkid
        -- LEFT OUTER JOIN writtenworkinfo wwi ON wwi.writtenworkid = cri.writtenworkid
        -- LEFT OUTER JOIN logininfo li ON li.loginid = cri.studentid
        -- LEFT OUTER JOIN studentinfo si ON si.username = li.username
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

    queryset = models.Schoolinfo.objects.all().order_by('schoolname')
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

    queryset = models.RubricsHeader.objects.all().order_by('-slno')
    serializer_class = adminserializers.AdminrubricsSerializer

    def create(self, request):
        adminrubrics = models.RubricsHeader()
        rubricmatrix = models.RubricMatrix()
        rubricsdata =  json.loads(request.DATA.keys()[0])
        rubbodydata = rubricsdata.get('mtx_body')
        rubheaderdata = rubricsdata.get('mtx_head')
        
        adminrubrics.title = rubricsdata.get('instn')
        adminrubrics.description = rubricsdata.get('desc')
        adminrubrics.instruction = rubricsdata.get('instn')
        adminrubrics.teacher = request.user.username
        adminrubrics.status = 0
        adminrubrics.ts = time.strftime('%Y-%m-%d %H:%M:%S')
        adminrubrics.save()

        refno = adminrubrics.slno

        for idx, bd in enumerate(rubbodydata):
            rubricmatrix.refno = refno
            rubricmatrix.datatype = 'B'
            rubricmatrix.jdata = bd
            rubricmatrix.disp_order = idx+1
            rubricmatrix.save()

        for idy, hd in enumerate(rubheaderdata):
            rubricmatrix.refno = refno
            rubricmatrix.datatype = 'H'
            rubricmatrix.jdata = hd
            rubricmatrix.disp_order = idy
            rubricmatrix.save()

        return Response(request.DATA);

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class AssignresourceinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Assignresourceinfo.objects.all()
    serializer_class = adminserializers.AssignresourceinfoSerializer

    def list(self, request):
        resourceid = request.GET.get('resourceid')
       
        if resourceid :
            queryset = models.Assignresourceinfo.objects.filter(resourceid=resourceid)
        else:
            queryset = models.Assignresourceinfo.objects.all()
        serializer = adminserializers.AssignresourceinfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        assignresourceinfo = models.Assignresourceinfo()
        assigndata =  json.loads(request.DATA.keys()[0])
        assignresourceinfo.resourceid = assigndata.get('resourceid')
        assignresourceinfo.isdelete = 0 #assigndata.get('IsDelete')
        assignresourceinfo.assignedby = assigndata.get('assignedby')
        assignresourceinfo.assigneddate = time.strftime('%Y-%m-%d %H:%M:%S')
        assignresourceinfo.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')
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
        cal.color = '#337ab7'
        cal.allday = data.get('alldayevents')
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
        cal.color = '#d9534f'
        cal.allday = data.get('alldayevents')
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
    def destroy(self, request, pk):
        models.Calendardetails.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

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
               ari.answerurl,
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
        GROUP BY ari.resourceid, ari.answereddate
        ORDER BY ari.assignedid DESC''' % (request.user.username, datecond)
        cursor = connection.cursor()
        
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
               ari.rubric_id,
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
               ari.isbillboard,
               ari.isclassroom,
               ari.rubric_marks,
               ari.rubric_n_mark,
               ari.answerurl
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
        l =  request.user.groups.values_list('name',flat=True)[0]
        fieldcond=""
        joincond=""
        wherecond = ""
        if l == 'Admin' or l == 'Teacher' :
            fieldcond="au.first_name AS postedby"
            joincond="INNER JOIN auth_user au ON au.username = bmi.userid"
            wherecond = "bmi.userid = '%s'"%request.user.username
        else:
            fieldcond="'' AS postedby"
            joincond=""
            wherecond = """bmi.schoolid = '%s'
                           AND bmi.classid = '%s' 
                        """%(request.session.get('stu_schoolid'), 
                             request.session.get('stu_classid'))

        sql = """
        SELECT  bbi.bulletinboardid,
                bbi.messagetitle,
                bbi.message,
                bbi.attachmenturl,
                %s,
                DATE(bbi.posteddate ) AS posteddate
        FROM bulletinboardinfo bbi
        INNER JOIN bulletinmappinginfo bmi ON bbi.bulletinboardid = bmi.bulletinboardid
        %s
        WHERE %s
        GROUP BY bbi.bulletinboardid
        ORDER by bbi.bulletinboardid DESC
        LIMIT 2"""% (fieldcond,joincond,wherecond)
        # print sql;
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
        bbi.attachmenturl = data.get('attachmenturl',0)
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
        #print "created id is %s"%bbi.bulletinboardid
        #saving annoument target
        for rl in data.get('resourcelist'):
            bmi = models.Bulletinmappinginfo()
            bmi.bulletinboardid = bbiid
            bmi.viewtype = 0    
            bmi.postedby = request.user.id
            bmi.userid = request.user.username
            if data.get('cattype') == 'schools':
                bmi.schoolid = data.get('schoolid')
                bmi.classid = rl
            else:
                bmi.schoolid = 0
                bmi.classid = 0
            bmi.save()

        for rl in data.get('resourcelist'):
            bmi = models.Bulletinmappinginfo()
            bmi.bulletinboardid = bbiid
            bmi.viewtype = 0    
            bmi.postedby = request.user.id
            if data.get('cattype') == 'schools':
                bmi.schoolid = data.get('schoolid')
                bmi.classid = rl
                bmi.userid = 0
            else:
                bmi.schoolid = 0
                bmi.classid = 0
                bmi.userid = rl
            bmi.save()
        return Response(request.DATA)

    def retrieve(self, request, pk=None):
        queryset = models.Bulletinboardinfo.objects.filter(pk=pk)[0]
        serializer = adminserializers.BulletinboardlistinfoSerializer(queryset, many=False)
        return Response(serializer.data)    

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
        ORDER BY bbi.billboardid desc 
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
                ci.classid AS classid 
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
        import MySQLdb
        assignedid = request.GET.get('assignedid')

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

        sql = '''
        SELECT previoustext
        FROM editingtext 
        WHERE spanid = '%s'
            AND isapproved = 1 ''' % (str(spanid))
        cursor = connection.cursor()
        cursor.execute(sql)
        result =  cursor.fetchone()
        if result:
            previoustext = result[0];

        approvedanswertext = answertext.replace(previoustext,edittext)

        #updating approved answer text
        sql = '''
        UPDATE assignresourceinfo 
           SET answertext = '%s'
           WHERE assignedid = '%s' ''' % (MySQLdb.escape_string(approvedanswertext), assignedid)
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
        assignedresourceid = request.GET.get('assignedresourceid');
        billboard.resourceid = assignedresourceid
        billboard.resourcetype = 'ar'
        billboard.studentid = str(studentid)
        billboard.votescount = 0
        billboard.lastvotedby = 0
        billboard.postedby = str(request.user.username)
        billboard.posteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        billboard.save()

        sql = '''
        UPDATE assignresourceinfo
            SET isbillboard = 1
        WHERE assignedid = '%s' ''' % (assignedresourceid)

        cursor = connection.cursor()
        cursor.execute(sql)        

        return Response('saved')

class TopicViewSet(viewsets.ModelViewSet):

    queryset = models.Topicinfo.objects .all()
    serializer_class = adminserializers.TopicsSerializer

    def list(self, request):
        topicid = request.GET.get('topicid')
        topicname = request.GET.get('topicname')
        if topicid :
            queryset = models.Topicinfo.objects.filter(topicid=topicid)
        else:
            queryset = models.Topicinfo.objects.all()
        serializer = adminserializers.TopicsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        topics = models.Topicinfo()
        topicinfodata =  json.loads(request.DATA.keys()[0])
        topics.topicid = topicinfodata.get('topicid',0)
        topics.forumid = topicinfodata.get('forumid',0)
        topics.totalpost = topicinfodata.get('totalpost',0)
        topics.forumid = topicinfodata.get('forumid',0)
        topics.topicname = topicinfodata.get('topicname',0)
        topics.createdby = request.user.id
        topics.lastpostedby = request.user.id
        topics.lastposteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        topics.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        topics.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')
        
class ThreadsViewSet(viewsets.ModelViewSet):

    queryset = models.Threaddetails.objects.all()
    serializer_class = adminserializers.ThreadSerializer

    def list(self, request):
        topicid = request.GET.get('topicid')
        topicname = request.GET.get('topicname')
       
        if topicid :
            queryset = models.Threaddetails.objects.filter(topicid=topicid)
        else:
            queryset = models.Threaddetails.objects.all()
        serializer = adminserializers.ThreadSerializer(queryset, many=True)
        return Response(serializer.data)

    
    def retrieve(self, request, pk=None):
        threadid = request.GET.get('threadid')
        threadname = request.GET.get('threadname')

        sql = """
        SELECT td.threadid,ti.topicname,td.threadname
        FROM threaddetails td 
        LEFT JOIN topicinfo ti ON ti.topicid =  td.topicid
        where td.threadid=%s
        """ % pk

        cursor = connection.cursor()
        # print sql
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

        #queryset = models.Threaddetails.objects.get(pk=pk)
        #serializer = adminserializers.ThreadSerializer(queryset, many=False)
        #return Response(serializer.data)

    def create(self, request):
        thread = models.Threaddetails()
        threaddetailsdata =  json.loads(request.DATA.keys()[0])
        thread.threadid = threaddetailsdata.get('threadid',0)
        thread.topicid = threaddetailsdata.get('topicid',0)
        thread.threadname = threaddetailsdata.get('threadname',0)
        thread.createdby = request.user.id
        thread.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        thread.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')


class RubricsViewSet(viewsets.ModelViewSet):

    queryset = models.RubricsHeader.objects.all()
    serializer_class = adminserializers.AdminrubricsSerializer

    def retrieve(self, request, pk=None):
        data = {}

        sql = '''
        SELECT *
        FROM rubrics_header
        WHERE slno = %s
        ''' % pk

        cursor = connection.cursor()
        cursor.execute(sql)
        data['rh'] =  cursor.fetchone()
        
        sql = '''
        SELECT jdata
        FROM rubric_matrix
        WHERE refno = %s
        AND datatype='H'
        ''' % pk

        cursor = connection.cursor()
        cursor.execute(sql)
        data['rmh'] =  cursor.fetchone()

        sql = '''
        SELECT jdata 
        FROM rubric_matrix
        WHERE refno = %s 
        AND datatype='B' 
        ORDER BY disp_order
        ''' % pk

        cursor = connection.cursor()
        cursor.execute(sql)
        data['rmb'] =  cursor.fetchall()

        return Response(data)

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
        data = json.loads(request.DATA.keys()[0])
        arirm = models.Assignresourceinfo.objects.get(pk=pk)
        arirm.rubric_marks    = data.get('ans')
        arirm.rubric_n_mark   = data.get('ans_n')
        arirm.save()
        return Response({'msg':True})

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class ExtraslistViewSet(viewsets.ModelViewSet):
    queryset = models.Extraslist.objects.all()
    serializer_class = adminserializers.ExtraslistSerializer

    def list(self, request):
        categorytype   = request.GET.get('type')
        classid   = request.GET.get('classid')
        section = request.GET.get('section')
       
        sql = """
        SELECT  el.extraid,
                el.classid,
                el.section,
                el.resourceurl,
                el.title,
                el.extratype,
                li.firstname,
                date(el.createddate) as createddate 
        FROM extraslist el
        INNER JOIN logininfo li ON li.loginid=el.createdby  
        WHERE li.isdelete=0 
        -- AND el.extratype = '%s' 
        AND el.classid=%s 
        AND el.section='%s' 
        ORDER BY el.extraid DESC
        """ % (categorytype,classid,section) 
        cursor = connection.cursor()
        # print sql
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

class StickyinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Stickyinfo.objects.all()
    serializer_class = adminserializers.StickyinfoSerializer

    def create(self, request):
        stickylist = models.Stickyinfo()
        stickydata =  json.loads(request.DATA.keys()[0])
        stickylist.title = stickydata.get('title')
        stickylist.isdeleted = 0
        stickylist.createdby = request.user.id
        stickylist.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        stickylist.save()
        return Response(request.DATA)

class AuthuserViewSet(viewsets.ModelViewSet):

    queryset = models.Auth_user.objects.all()
    serializer_class = adminserializers.Auth_userSerializer

    def list(self, request):
        id = request.GET.get('id')
       
        if id :
            queryset = models.Auth_user.objects.filter(id=id)
        else:
            queryset = models.Auth_user.objects.all()
        serializer = adminserializers.Auth_userSerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        userid   = request.user.id
        # print userid
        return Response(userid)


    def create(self, request):
        authuser = models.Auth_user()
        authuserdata =  json.loads(request.DATA.keys()[0])
        authuser.id = authuserdata.get('id')
        authuser.password = authuserdata.get('password')
        authuser.last_login = time.strftime('%Y-%m-%d %H:%M:%S')
        authuser.username = authuserdata.get('username')
        authuser.firstname = authuserdata.get('firstname')
        authuser.last_name = authuserdata.get('last_name')
        authuser.email = authuserdata.get('email')
        authuser.is_staff = authuserdata.get('is_staff')
        authuser.is_active = authuserdata.get('is_active')
        authuser.date_joined = time.strftime('%Y-%m-%d %H:%M:%S')
        authuser.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        # print "*"*80
        # print request.DATA
        authuser = models.Auth_user.objects.get(pk=pk)
        authuserdata =  json.loads(request.DATA.keys()[0])
        authuser.password = authuserdata.get('password')
        authuser.email = authuserdata.get('firstname')
        authuser.emailid = authuserdata.get('emailid')
        authuser.save()
        return Response(request.DATA)

class AudioinfoViewSet(viewsets.ViewSet):

    queryset = models.Admininfo.objects.filter(isdelete=0).order_by('-createddate')
    serializer_class = adminserializers.AudiouploadSerializer
    def perform_authentication(self, request):
        pass
    
    def create(self, request):
        queryset = models.Admininfo.objects.filter(isdelete=0).order_by('-createddate')
        serializer_class = adminserializers.AudiouploadSerializer
    
        import os, time
        f = request.FILES["upload_file[filename]"]
        filename = request.POST.get("uploadfilename")
        ts = time.time()
        filename = filename+str(ts)+'.wav'
        fullpath = os.path.join('static/audio', filename)
        with open(fullpath, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return Response({'filename':filename})


class AdminresourceViewSet(viewsets.ModelViewSet):

    queryset = models.AdminResources.objects.filter(isdeleted=0).order_by('-createddate')
    serializer_class = adminserializers.AdminresourceSerializer

    def create(self, request):
        admin = models.AdminResources()
        admindata =  json.loads(request.DATA.keys()[0])
        admin.resourcetype = admindata.get('resourcetype')
        admin.resourcetitle = admindata.get('resourcetitle')
        admin.resourcedescription = admindata.get('resourcedescription')
        admin.documenturl = 0
        admin.imageurl = 0
        admin.audiourl = 0
        admin.videourl = 0
        admin.isdeleted = 0
        admin.resource_folder_id = admindata.get('resource_folder_id')
        admin.fileurl = admindata.get('fileurl')
        admin.createdby = request.user.id
        admin.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        admin.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk):
        models.Admininfo.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

class ClassinfoViewSet(viewsets.ModelViewSet): 
    queryset = models.Classroominfo.objects.all()
    serializer_class = adminserializers.ClassroominfoSerializer

    def create(self, request):
        classroom = models.Classroominfo()
        classroomdata =  json.loads(request.DATA.keys()[0])
        classroom.resourceid            = classroomdata.get('assignedresourceid')
        classroom.resourcetype          = 'ar'        
        classroom.studentid             = str(classroomdata.get('studentid'))
        classroom.rating                = 0
        classroom.ratingcount           = 0
        classroom.votescount            = 0
        classroom.lastvotedby           = 0
        classroom.postedby              = str(request.user.username)
        classroom.schoolid              = request.session.get('stu_schoolid')
        classroom.classid               = request.session.get('stu_classid')
        classroom.posteddate            = time.strftime('%Y-%m-%d %H:%M:%S')
        classroom.save()

        sql = '''
        UPDATE assignresourceinfo
            SET isclassroom = 1
        WHERE assignedid = '%s' ''' % (classroomdata.get('assignedresourceid'))
        cursor = connection.cursor()
        cursor.execute(sql)

        return Response(request.DATA)

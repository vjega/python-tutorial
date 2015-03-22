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

def summer_decode(str):
    return str.replace('~',':').replace('#','=').replace('^',';').replace('*','&')

def add_activitylog(request, data):
    activitylog = models.Activitylog()
    activitylog.loginid         = request.user.username
    activitylog.pagename        = request.user.groups.values_list('name',flat=True)[0].lower()+"/"+data['pagename']
    activitylog.operation       = data['operation']
    activitylog.usertype        = request.user.groups.values_list('name',flat=True)[0]
    activitylog.stringsentence  = data['stringsentence']
    activitylog.updateddate     = time.strftime('%Y-%m-%d %H:%M:%S')
    activitylog.save()

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

        aldata = {}
        aldata['pagename']       = 'adminlist'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Admin Created'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    @delete_login('Admin')
    def destroy(self, request, pk):
        models.Admininfo.objects.get(pk=pk).delete()

        aldata = {}
        aldata['pagename']       = 'adminlist'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a Admin'
        add_activitylog(request, aldata)
        
        return Response('"msg":"delete"')

class AdminFoldersViewSet(viewsets.ModelViewSet):

    queryset = models.AdminFolders.objects.all()
    serializer_class = adminserializers.AdminFolderSerializer

    def create(self, request):
        adminfolder = models.AdminFolders()
        data =  json.loads(request.DATA.keys()[0])
        adminfolder.folder_name = data.get('folder_name')
        adminfolder.folder_description = data.get('folder_name')
        adminfolder.folder_order = 1#data.get('order_no')
        adminfolder.added_date = time.strftime('%Y-%m-%d %H:%M:%S')
        adminfolder.userid = request.user.username
        adminfolder.save()
        
        aldata = {}
        aldata['pagename']       = 'adminlist'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Folder Created'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    def destroy(self, request, pk):
        models.AdminFolders.objects.get(pk=pk).delete()
        
        aldata = {}
        aldata['pagename']       = 'adminlist'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a Folder'
        add_activitylog(request, aldata)

        return Response('"msg":"delete"')

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = models.Teacherinfo.objects.all()
    serializer_class = adminserializers.TeacherinfoSerializer
    def list(self, request):
        schoolid =  request.GET.get('schoolid')
        classid  =  request.GET.get('classid')
        username = request.GET.get('username')
       
        if schoolid and classid and username:
            queryset = models.Teacherinfo.objects.filter(schoolid=schoolid, classid=classid, isdelete=0).order_by('-createddate')
        elif schoolid:
            queryset = models.Teacherinfo.objects.filter(schoolid=schoolid, isdelete=0).order_by('-createddate')
        elif username:
            queryset = models.Teacherinfo.objects.filter(username=username, isdelete=0)

        else:
            queryset = models.Teacherinfo.objects.filter(isdelete=0)

        serializer = adminserializers.TeacherinfoSerializer(queryset, many=True)
        return Response(serializer.data)

    @create_login('Teacher')
    def create(self, request):
        teacher = models.Teacherinfo()
        teacherdata =  json.loads(request.DATA.keys()[0])
        teacher.username = teacherdata.get('username')
        teacher.lastname = '' #teacherdata.get('lastname')
        teacher.password = teacherdata.get('password')
        teacher.firstname = teacherdata.get('firstname')
        teacher.schoolid = teacherdata.get('schoolid')
        teacher.classid = teacherdata.get('classid')
        teacher.section = teacherdata.get('section')
        teacher.emailid = teacherdata.get('emailid')
        teacher.imageurl = teacherdata.get('imageurl')
        #teacher.imageurl = #studentdata.get('imageurl')
        teacher.isdelete = 0
        teacher.createdby = request.user.id
        teacher.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        teacher.save()

        aldata = {}
        aldata['pagename']       = 'teacherslist'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Teacher Created'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    def update(self, request, pk=None):
        #print request.GET.get('schoolid');
        teacher = models.Teacherinfo.objects.get(pk=pk)
        teacherdata =  json.loads(request.DATA.keys()[0])
        teacher.username = teacherdata.get('username')
        teacher.lastname = teacherdata.get('lastname')
        teacher.password = teacherdata.get('password')
        teacher.firstname = teacherdata.get('firstname')
        teacher.schoolid = teacherdata.get('schoolid')
        teacher.imageurl = teacherdata.get('imageurl')
        teacher.classid = teacherdata.get('classid')
        teacher.section = teacherdata.get('section')
        teacher.emailid = teacherdata.get('emailid')
        teacher.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        teacher.save()

        aldata = {}
        aldata['pagename']       = 'teacherslist'
        aldata['operation']      = 'Update'
        aldata['stringsentence'] = 'Updated a Teacher'

        return Response(request.DATA)

    def partial_update(self, request, pk=None):
        # print "Hi"
        pass

    @delete_login('Teacher')
    def destroy(self, request, pk):
        teacher = models.Teacherinfo.objects.get(pk=pk)
        teacher.isdelete = 1
        teacher.save()

        aldata = {}
        aldata['pagename']       = 'teacherslist'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a Teacher'

        return Response('"msg":"delete"')


class studentViewSet(viewsets.ModelViewSet):
    queryset = models.Studentinfo.objects.filter(isdelete=0)
    serializer_class = adminserializers.StudentinfoSerializer
    
    def list(self, request):
        schoolid =  request.GET.get('schoolid')
        classid  =  request.GET.get('classid')
        section  =  request.GET.get('section')
        schoolids  =  request.GET.get('schoolids')

        if schoolid and classid and section:
            queryset = models.Studentinfo.objects.filter(schoolid=schoolid, classid=classid, section=section, isdelete=0).order_by('-createddate')
        elif schoolid:
            queryset = models.Studentinfo.objects.filter(schoolid=schoolid, isdelete=0).order_by('-createddate')
        elif schoolids:
            schools = schoolids.split(",")
            q = Q()
            for s in schools:
                q |= Q(schoolid=s)
            queryset = models.Studentinfo.objects.filter(q, classid=classid, isdelete=0)
        else:
            queryset = models.Studentinfo.objects.filter(isdelete=0)
        
        serializer = adminserializers.StudentinfoSerializer(queryset, many=True)
        return Response(serializer.data)
       
    @create_login('Student')
    def create(self, request):
        student = models.Studentinfo()
        studentdata =  json.loads(request.DATA.keys()[0])
        student.schoolid = studentdata.get('schoolid')
        student.classid = studentdata.get('classid')
        student.section = studentdata.get('section')
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
        
        aldata = {}
        aldata['pagename']       = 'studentlist'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Student Created'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    def update(self, request, pk=None):
        #print dir(request)
        student = models.Studentinfo.objects.get(pk=pk)
        studentdata =  json.loads(request.DATA.keys()[0])
        student.username = studentdata.get('username')
        student.lastname = studentdata.get('lastname')
        student.password = studentdata.get('password')
        student.firstname = studentdata.get('firstname')
        student.schoolid = studentdata.get('schoolid')
        student.classid = studentdata.get('classid')
        student.section = studentdata.get('section')
        student.emailid = studentdata.get('emailid')
        student.imageurl = studentdata.get('imageurl')
        student.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        student.save()

        # authuser = models.Auth_user.objects.get(username=studentdata.get('username'))
        # authuserdata =  json.loads(request.DATA.keys()[0])
        # authuser.password = User.set_password(authuserdata.get('password'))
        # authuser.first_name = authuserdata.get('firstname')
        # authuser.emailid = authuserdata.get('emailid')
        # authuser.save()

        aldata = {}
        aldata['pagename']       = 'studentlist'
        aldata['operation']      = 'Update'
        aldata['stringsentence'] = 'Updated a Student'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    @delete_login('Student')
    def destroy(self, request, pk=None):
        student = models.Studentinfo.objects.get(pk=pk)
        student.isdelete = 1
        student.save()
        
        aldata = {}
        aldata['pagename']       = 'studentlist'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a Student'
        add_activitylog(request, aldata)
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
        l =  request.user.groups.values_list('name',flat=True)[0]
        # schoolid   = request.GET.get('schoolid')
        # classid   = request.GET.get('classid')
        # section   = request.GET.get('section')
        # chapterid = request.GET.get('chapterid')
        # categoryid = request.GET.get('resourcecategory')
        joincond=''
        fieldcond=''
        schoolid    = ''
        classid     = ''
        section     = ''
        chapterid   = ''
        categoryid  = ''
        if l == 'Admin' :
            fieldcond="ci.shortname as levelname"
            joincond="INNER JOIN classinfo ci ON ci.classid=tri.classid"
        else :
            fieldcond="'' as levelname"

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
                %s,
                tri.resourcetype
        FROM teacherresourceinfo tri
        %s
        WHERE isdeleted=0
        %s 
        %s 
        %s 
        %s 
        %s
        ORDER BY tri.createddate DESC
        """ % (fieldcond,joincond,schoolid,classid,section,chapterid,categoryid)
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
        teacherresource.resourcetitle = summer_decode(teacherresourcedata.get('resourcetitle'))
        teacherresource.originaltext = summer_decode(teacherresourcedata.get('resourcetitle'))
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

        aldata = {}
        aldata['pagename']       = 'viewteacherres'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Tacher Resource Created'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        allschool = models.Teacherresourceinfo.objects.get(pk=pk)
        allschool.isdeleted = 1
        allschool.save()

        aldata = {}
        aldata['pagename']       = 'viewteacherres'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a Resource'
        add_activitylog(request, aldata)

        return Response('"msg":"delete"')

    def retrieve(self, request, pk=None):
        queryset = models.Teacherresourceinfo.objects.get(pk=pk)
        serializer = adminserializers.TeacherresourceinfoSerializer(queryset, many=False)
        return Response(serializer.data)


class StudentWrittenWorkDetailViewSet(viewsets.ModelViewSet):
    queryset = models.Writtenworkinfo.objects.all()
    serializer_class = adminserializers.WrittenworkinfoSerializer
    
    def list(self, request):
        classid   = request.GET.get('classid')
        section   = request.GET.get('section')
        chapterid = request.GET.get('chapterid')
        categoryid = request.GET.get('categoryid')
        writtenworkid = request.GET.get('writtenworkid')
        studentid = request.GET.get('studentid')
        kwarg = {}
        kwarg['isdeleted'] = 0
        wherecond = '';
        if classid:
            wherecond += " AND wwi.classid = "+classid
        if section:
            wherecond += " AND wwi.section = "+section
        if chapterid:
            wherecond += " AND wwi.chapterid = "+chapterid
        if categoryid:
            wherecond += " AND wwi.categoryid = "+categoryid
        if writtenworkid:
            wherecond += " AND wwi.writtenworkid = "+writtenworkid            
        if studentid:
            wherecond += " AND awwi.studentid = '"+studentid+"'"

        # queryset = models.Resourceinfo.objects.filter(**kwarg).order_by('-createddate')
        # serializer = adminserializers.ResourceinfoSerializer(queryset, many=True)
        #print queryset;

        sql = '''
        SELECT wwi.*,
            awwi.studentid
        FROM assignwrittenworkinfo awwi
        INNER JOIN writtenworkinfo wwi on wwi.writtenworkid = awwi.assignwrittenworkid 
        WHERE isdeleted=0
              %s
        GROUP BY wwi.writtenworkid, awwi.answereddate
        ORDER BY awwi.assignwrittenworkid DESC''' % (wherecond)

        print sql

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        return Response(result)        


class StudentAssessmentDetailViewSet(viewsets.ModelViewSet):
    queryset = models.Writtenworkinfo.objects.all()
    serializer_class = adminserializers.WrittenworkinfoSerializer
    
    def list(self, request):
        classid   = request.GET.get('classid')
        section   = request.GET.get('section')
        chapterid = request.GET.get('chapterid')
        categoryid = request.GET.get('categoryid')
        assessmentid = request.GET.get('assessmentid')
        studentid = request.GET.get('studentid')
        kwarg = {}
        kwarg['isdeleted'] = 0
        wherecond = '';
        if classid:
            wherecond += " AND ai.classid = "+classid
        if section:
            wherecond += " AND ai.section = "+section
        if chapterid:
            wherecond += " AND ai.chapterid = "+chapterid
        if categoryid:
            wherecond += " AND ai.categoryid = "+categoryid
        if assessmentid:
            wherecond += " AND aai.assessmentid = "+assessmentid            
        if studentid:
            wherecond += " AND aai.studentid = '"+studentid+"'"

        # queryset = models.Resourceinfo.objects.filter(**kwarg).order_by('-createddate')
        # serializer = adminserializers.ResourceinfoSerializer(queryset, many=True)
        #print queryset;

        sql = '''
        SELECT ai.*,
            aai.studentid
        FROM assignassessmentinfo aai
        INNER JOIN assessmentinfo ai on ai.id = aai.assessmentid 
        WHERE isdeleted=0
              %s
        GROUP BY ai.id, aai.answereddate
        ORDER BY aai.assessmentid DESC''' % (wherecond)

        print sql

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        return Response(result)                


class ResourceStudentinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Resourceinfo.objects.all()
    serializer_class = adminserializers.ResourceinfoSerializer
    
    def list(self, request):
        classid   = request.GET.get('classid')
        section   = request.GET.get('section')
        chapterid = request.GET.get('chapterid')
        categoryid = request.GET.get('categoryid')
        resourceid = request.GET.get('resourceid')
        studentid = request.GET.get('studentid')
        kwarg = {}
        kwarg['isdeleted'] = 0
        wherecond = '';
        if classid:
            wherecond += " AND ri.classid = "+classid
        if section:
            wherecond += " AND ri.section = "+section
        if chapterid:
            wherecond += " AND ri.chapterid = "+chapterid
        if categoryid:
            wherecond += " AND ri.categoryid = "+categoryid
        if studentid:
            wherecond += " AND ari.studentid = '"+studentid+"'"

        # queryset = models.Resourceinfo.objects.filter(**kwarg).order_by('-createddate')
        # serializer = adminserializers.ResourceinfoSerializer(queryset, many=True)
        #print queryset;

        sql = '''
        SELECT ri.*,
            ari.studentid
        FROM assignresourceinfo ari
        INNER JOIN  resourceinfo ri on ri.resourceid = ari.resourceid 
        WHERE isdeleted=0
              AND ari.IsDelete=0
              %s
        GROUP BY ari.resourceid, ari.answereddate
        ORDER BY ari.assignedid DESC''' % (wherecond)

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        return Response(result)        

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

        queryset = models.Resourceinfo.objects.filter(**kwarg).order_by('-createddate')
        serializer = adminserializers.ResourceinfoSerializer(queryset, many=True)
        #print queryset;
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = models.Resourceinfo.objects.get(pk=pk)
        serializer = adminserializers.ResourceinfoSerializer(queryset, many=False)
        return Response(serializer.data)


    def create(self, request):
        ri = models.Resourceinfo()
        # print request.DATA, type(request.DATA)
        ridata =  json.loads(dict(request.DATA).keys()[0])
        category = ridata.get('categoryid')
        if category == 'text' :
            categoryid = 0
        elif category == 'image':
            categoryid = 1
        # elif category == 'audio':
        #     categoryid = 2
        elif category == 'video':
            categoryid = 2

        ri.categoryid = categoryid
        ri.classid = int(ridata.get('classid'))
        ri.section = ridata.get('section')
        ri.chapterid = ridata.get('chapterid')
        ri.resourcetype = category
        ri.chapterid = ridata.get('chapterid')
        ri.resourceid = ridata.get('resourceid')
        ri.resourcetitle = summer_decode(ridata.get('resourcetitle'))
        ri.resourcedescription = summer_decode(ridata.get('resourcedescription', ""))
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

        aldata = {}
        aldata['pagename']       = 'viewstudentres'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Student Resource Created'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    def destroy(self, request, pk=None):
        studentres = models.Resourceinfo.objects.get(pk=pk)
        studentres.isdeleted = 1
        studentres.save()

        aldata = {}
        aldata['pagename']       = 'viewstudentres'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a Resource'
        add_activitylog(request, aldata)

        return Response('"msg":"delete"')

class WrittenworkinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Writtenworkinfo.objects.all()
    serializer_class = adminserializers.WrittenworkinfoSerializer

    def list(self, request):
        # queryset = models.Writtenworkinfo.objects.filter(createdby=str(request.user.username)).order_by('-createddate')
        # serializer = adminserializers.WrittenworkinfoSerializer(queryset, many=True)
        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (wwi.createddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))
        sql = '''
        SELECT assignwrittenworkid AS id,
               wwi.writtenworkid,
               wwi.writtenImage,
               wwi.writtenworktitle,
               wwi.createddate as createddate,
               awwi.studentid,
               wwi.isassigned,
               awwi.issaved
        FROM assignwrittenworkinfo awwi
        INNER JOIN writtenworkinfo wwi on wwi.writtenworkid = awwi.writtenworkid 
        WHERE wwi.createdby = '%s'
        %s
        GROUP BY awwi.writtenworkid
        ORDER BY wwi.createddate DESC
        ''' % (request.user.username,datecond)
        cursor = connection.cursor()
        cursor.execute(sql)
        #print sql;
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

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
        students = data.get('students')
        title = data.get('title')
        title = summer_decode(title)
        note = data.get('note')
        note = summer_decode(note)
        schoolid = request.session.get('schoolid')
        classid = request.session.get('classid')

        if data.get('rubricid'):
            rubric_id = data.get('rubricid')
        else:
            rubric_id = 0

        if data.get('attachmenturl'):
            attachmenturl = data.get('attachmenturl')
        else:
            attachmenturl = 0

        writtenwork = models.Writtenworkinfo()
        writtenwork.writtenworktitle= unicode(title)
        writtenwork.description     = unicode(note)
        writtenwork.writtenimage    = attachmenturl
        writtenwork.schoolid        = schoolid
        writtenwork.classid         = classid
        writtenwork.isassigned      = 0
        writtenwork.isdeleted       = 0
        writtenwork.answereddate    = '1910-01-01'
        writtenwork.createdby       = str(request.user.username)
        writtenwork.createddate     = time.strftime('%Y-%m-%d %H:%M:%S')
        writtenwork.save()

        writtenworkid = writtenwork.writtenworkid
        for s in students:
            awwi = models.Assignwrittenworkinfo()
            awwi.writtenworkid = writtenworkid
            awwi.studentid = unicode(s)
            awwi.assigntext = unicode(note)
            awwi.issaved = 0
            awwi.ispublished = 0
            awwi.isrecord = 0
            awwi.answerrating = 0
            awwi.isbillboard = 0
            awwi.isclassroom = 0
            awwi.rubric_id = rubric_id
            awwi.isanswered = 0
            awwi.answereddate = '1910-01-01'
            awwi.assignedby = str(request.user.username)
            awwi.assigneddate = time.strftime('%Y-%m-%d %H:%M:%S')
            awwi.publisheddate = time.strftime('%Y-%m-%d %H:%M:%S')
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
        resourcecategory = request.GET.get('resourcecategory',0)
        #print resourcecategory;
        
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
        if resourcecategory:
            sql = '''
            SELECT chapterid, 
                   count(*) AS cnt
            FROM teacherresourceinfo 
            WHERE classid=%s
                AND section='%s' 
                AND isdeleted=0
                AND resourcecategory=%s
            GROUP BY chapterid
            ORDER BY chapterid
            '''%(classid, sectionid,resourcecategory)
        else:
            sql = '''
            SELECT chapterid, 
                   count(*) AS cnt
            FROM resourceinfo 
            WHERE categoryid=%s
                AND classid=%s
                AND section='%s' 
                AND isdeleted=0
            GROUP BY chapterid
            ORDER BY chapterid
            '''%(categoryid, classid, sectionid)
        #print sql;
        cursor = connection.cursor()
        cursor.execute(sql)
        cnt = cursor.fetchall()
        for i, d in enumerate(serializer.data):
            serializer.data[i]['rescount']=0
            for c in cnt:
                if serializer.data[i]['chapterid'] == c[0]:
                    serializer.data[i]['rescount'] = c[1]
                    break
            # print serializer.data
        return Response(serializer.data)

     # def retrieve(self, request, pk=None):
     #    queryset = models.Chapterinfo.objects.filter(pk=pk)[0]
     #    serializer = adminserializers.ChapterinfoSerializer(queryset, many=False)
     #    return Response(serializer.data)
 
class AdminschoolViewSet(viewsets.ModelViewSet):

    queryset = models.Schoolinfo.objects.all().order_by('schoolname')
    serializer_class = adminserializers.AdminschoolSerializer

    def create(self, request):
        adminschools = models.Schoolinfo()
        schooldata =  json.loads(request.DATA.keys()[0])
        adminschools.schoolname = schooldata.get('schoolname')
        adminschools.shortname = schooldata.get('shortname')
        adminschools.description = schooldata.get('schoolname')
        adminschools.createdby = request.user.id
        adminschools.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        adminschools.save()

        aldata = {}
        aldata['pagename']       = 'Schoollist'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New School Created'
        add_activitylog(request, aldata)

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

        aldata = {}
        aldata['pagename']       = 'Schoollist'
        aldata['operation']      = 'Update'
        aldata['stringsentence'] = 'Updated a sSchool'
        add_activitylog(request, aldata)


        return Response(request.DATA)


    def destroy(self, request, pk=None):
        models.Schoolinfo.objects.get(pk=pk).delete()

        aldata = {}
        aldata['pagename']       = 'Schoollist'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a School'
        add_activitylog(request, aldata)


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
        models.Classinfo.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

    def retrieve(self, request, pk=None):
        queryset = models.Classinfo.objects.filter(pk=pk)[0]
        serializer = adminserializers.AdminclasslistSerializer(queryset, many=False)
        return Response(serializer.data)

class AdminrubricsViewSet(viewsets.ModelViewSet):

    queryset = models.RubricsHeader.objects.all().order_by('-slno')
    serializer_class = adminserializers.AdminrubricsSerializer

    def create(self, request):
        adminrubrics = models.RubricsHeader()
        rubricmatrix = models.RubricMatrix()
        rubricsdata =  json.loads(request.DATA.keys()[0])

        rubbodydata = rubricsdata.get('mtx_body')
        rubheaderdata = rubricsdata.get('mtx_head')
        
        adminrubrics.title = rubricsdata.get('ttl')
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

        aldata = {}
        aldata['pagename']       = 'rubric_edit'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Rubrics Created'
        add_activitylog(request, aldata)

        return Response(request.DATA);

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        models.RubricsHeader.objects.get(pk=pk).delete()
        aldata = {}
        aldata['pagename']       = 'rubric_edit'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Delete a Rubrics'
        add_activitylog(request, aldata)

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
        startdt = data.get('start')+":00"
        enddt   = data.get('end')+":00"

        cal.title           = data.get('title')
        cal.start           = startdt
        cal.end             = enddt
        cal.color           = data.get('color')
        cal.allday          = data.get('alldayevents')
        cal.eventcreatedby  = request.user.username
        cal.eventeditedby   = request.user.username
        cal.isdeleted       = 0
        cal.createdby       = request.user.id
        cal.createddate     = time.strftime('%Y-%m-%d %H:%M:%S')
        cal.save()

        aldata = {}
        aldata['pagename']       = 'Calendar'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Event Created'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    def update(self, request, pk=None):
        cal = models.Calendardetails.objects.get(pk=pk)  
        data = json.loads(dict(request.DATA).keys()[0])
        #data = {k:v[0] for k,v in dict(request.DATA).items()}
        startdt             = data.get('start')+":00"
        enddt               = data.get('end')+":00"
        cal.title           = data.get('title')
        cal.start           = startdt
        cal.end             = enddt
        cal.color           = data.get('color')
        cal.allday          = data.get('alldayevents')
        cal.eventcreatedby  = request.user.username
        cal.eventeditedby   = request.user.username
        cal.isdeleted       = 0
        cal.createdby       = request.user.id
        cal.createddate     = time.strftime('%Y-%m-%d %H:%M:%S')
        cal.save()

        aldata = {}
        aldata['pagename']       = 'Calendar'
        aldata['operation']      = 'Update'
        aldata['stringsentence'] = 'Updated a Event'
        add_activitylog(request, aldata)


        return Response(request.DATA)
    def destroy(self, request, pk):
        models.Calendardetails.objects.get(pk=pk).delete()
        aldata = {}
        aldata['pagename']       = 'Calendar'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a Event'
        add_activitylog(request, aldata)
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

        aldata = {}
        aldata['pagename']       = 'mindmapedit'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Mindmap Created'
        add_activitylog(request, aldata)

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

        aldata = {}
        aldata['pagename']       = 'mindmapedit'
        aldata['operation']      = 'Update'
        aldata['stringsentence'] = 'Updated a Mindmap'
        add_activitylog(request, aldata)

        return Response(request.DATA)
        
    def destroy(self, request, pk):
        models.Mindmap.objects.get(pk=pk).delete()
        aldata = {}
        aldata['pagename']       = 'mindmapedit'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a Mindmap'
        add_activitylog(request, aldata)
        return Response('"msg":"delete"')


class StudentAssignResource(viewsets.ModelViewSet):
    queryset = models.Assignresourceinfo.objects.all()
    serializer_class = adminserializers.MindmapSerializer

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        
        ari = models.Assignresourceinfo.objects.get(pk=pk)
        
        ari.answertext = summer_decode(unicode(data.get('answertext')))

        if data.get('originaltext'):
            ari.originaltext = summer_decode(unicode(data.get('originaltext')))

        if data.get('answerurl'):
            ari.answerurl = unicode(data.get('answerurl'))
            ari.isrecord = 1

        if data.get('isanswered'):
            ari.isanswered = data.get('isanswered')
            ari.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')

        if data.get('issaved'):
            ari.issaved = data.get('issaved')
        
        ari.save()
        if data.get('spanid'):
            assignedid  = pk;
            spanid      = summer_decode(data.get('spanid'));
            fulltext    = summer_decode(data.get('fulltext'));
            orig        = summer_decode(data.get('orig'));
            modified    = summer_decode(data.get('modified'));
            usertype    = data.get('type');
            answertext  = summer_decode(data.get('answertext'));

            ar = models.Editingtext()
            ar.editid       = int(assignedid)
            ar.spanid       = unicode(spanid)
            ar.previoustext = unicode(orig)
            ar.edittext     = unicode(modified)
            ar.typeofresource = 0
            ar.isapproved   = 0
            ar.isrejected   = 0
            ar.editedby     = request.user.username
            ar.editeddate   = time.strftime('%Y-%m-%d %H:%M:%S')
            ar.usertype     = int(usertype)

            ar.save()

        aldata = {}
        aldata['pagename']       = 'viewassignresource'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'Answered For Resource'
        add_activitylog(request, aldata)

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
        #print sql;
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
               ari.assigntext,
               ari.studentid,
               ari.isanswered,
               ari.issaved,
               ari.rubric_id,
               ari.rubric_marks,
               ari.rubric_n_mark
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
        assigntext = summer_decode(data.get('assigntext'));

        for r in resource:
            for s in students:
                
                sql = """
                DELETE FROM assignresourceinfo 
                WHERE studentid='%s'
                AND resourceid='%s'
                """ % (str(s),int(r))

                cursor = connection.cursor()
                cursor.execute(sql)

                ar = models.Assignresourceinfo()
                ar.resourceid = int(r)
                ar.studentid = str(s)
                ar.assigntext = unicode(assigntext)
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
        

        aldata = {}
        aldata['pagename']       = 'assignchapter'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Resource Assigned to students'
        add_activitylog(request, aldata)

        return Response(request.DATA)


class TeacherStudentAssignResource(viewsets.ModelViewSet):
    queryset = models.Assignresourceinfo.objects.all()
    serializer_class = adminserializers.MindmapSerializer

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        #print data
        ari = models.Assignresourceinfo.objects.get(pk=pk)
        ari.originaltext    = summer_decode(unicode(data.get('originaltext')))
        ari.answertext      = summer_decode(unicode(data.get('answertext')))
        ari.answerurl       = data.get('answerurl')
        ari.isrecord        = 1
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
            datecond = "AND (ari.assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))

        sql = '''
        SELECT assignedid AS id,
               ri.resourceid,
               resourcetitle,
               ari.assigneddate as createddate,
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
              %s
        GROUP BY resourceid, ari.assigneddate
        ORDER BY assigneddate DESC''' % (request.user.username, datecond)

        #ORDER BY assigneddate DESC''' % (loginname_to_userid('Student', 'T0733732E'), datecond)
        cursor = connection.cursor()
        
        cursor.execute(sql)
        
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
        assigntext = summer_decode(data.get('assigntext'));
        #print resource
        #print students
        #print resource, students
        for r in resource:
            for s in students:

                sql = """
                DELETE FROM assignresourceinfo 
                WHERE studentid='%s'
                AND resourceid='%s'
                """ % (str(s),int(r))

                cursor = connection.cursor()
                cursor.execute(sql)

                ar = models.Assignresourceinfo()
                ar.resourceid = int(r)
                ar.studentid = str(s)
                ar.assigntext = unicode(assigntext)
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

    def destroy(self, request, pk):
        sql = '''
        UPDATE assignresourceinfo
        SET isDelete = 1
        WHERE resourceid = '%s'
        AND assigneddate='%s' 
        ''' % (pk,request.GET.get('createddate'))
        cursor = connection.cursor()
        cursor.execute(sql)
        return Response('"msg":"delete"')

class StickynotesResource(viewsets.ModelViewSet):
    queryset = models.stickynotes.objects.all()
    serializer_class = adminserializers.StickynotesSerializer

    def list(self, request):
        wherecond=''
        if request.GET.get('id'):
            wherecond="WHERE s.stickylistid=%s" % request.GET.get('id')
        sql = '''
        SELECT s.id,
            s.stickytext,
            s.attachment,
            s.color,
            group_concat(sc.id SEPARATOR "~") as commetid,
            group_concat(sc.stickycomment SEPARATOR "~") as comments,
            group_concat(sc.commentby SEPARATOR "~") as commentby,
            group_concat(sc.createddate SEPARATOR "~") as createddate
        FROM stickynotes s
        LEFT JOIN stickycomments sc ON sc.stickyid = s.id
        %s
        GROUP BY s.id, 
                 s.stickytext,
                 s.color, 
                 s.color
        ORDER BY s.createddate DESC''' %wherecond
        #print sql;
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
        stickynotes.stickylistid = data.get('stickylistid')
        stickynotes.stickytext = data.get('stickytext')
        stickynotes.attachment = data.get('attachment')
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
        stickynotes.attachment = data.get('attachment')
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

    def retrieve(self, request, pk=None):
        sql = '''
        SELECT  id,
                title
        FROM stickyinfo 
        WHERE id = %s
        ''' % pk
        cursor = connection.cursor()
        cursor.execute(sql)
        result = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
        return Response(result)

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
        studentinfo.section = rubricsdata.get('section')
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
        datetimecond = ''
        if request.GET.get('studentid'):
            studentcond = "AND ari.studentid = '" + request.GET.get('studentid') + "'"

        if request.GET.get('datetime'):
            datetimecond = "AND ari.assigneddate = " + request.GET.get('datetime') + ""

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
               ari.answerrating as rating,
               ari.answerurl
        FROM assignresourceinfo ari
        INNER JOIN  resourceinfo ri on ri.resourceid = ari.resourceid 
        INNER JOIN  auth_user au on au.username = ari.studentid 
        WHERE isdeleted=0
              AND ari.resourceid=%s
              AND ari.IsDelete=0 
              %s
              %s
        GROUP BY ari.studentid
        ORDER BY assigneddate DESC''' % (pk, studentcond, datetimecond)

        cursor = connection.cursor()
        cursor.execute(sql)
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
            joincond="INNER JOIN auth_user au ON au.id = bbi.postedby"
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
        """% (fieldcond,joincond,wherecond)
        cursor = connection.cursor()
        #print sql;
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
        bbi.messagetitle = summer_decode(data.get('messagetitle'))
        bbi.message = summer_decode(data.get('message'))
        bbi.attachmenturl = data.get('attachmenturl',0)
        if data.get('cattype') == 'schools':
            bbi.schoolid = data.get('schoolid')
        else:
            bbi.schoolid = 0 #data.get('schoolid')
        if data.get('cattype') == 'all_schools':
            bbi.allschool = data.get('allschool')
        else:
            bbi.allschool = 0
            bbi.schoolid = 0
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
        
        aldata = {}
        aldata['pagename']       = 'bulletinboard'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Announcement Created'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    def retrieve(self, request, pk=None):
        sql = """
        SELECT  bbi.bulletinboardid,
                bbi.messagetitle,
                bbi.message,
                bbi.attachmenturl,
                au.first_name as createdby,
                DATE(bbi.posteddate ) AS posteddate
        FROM bulletinboardinfo bbi
        LEFT JOIN  auth_user au ON au.id = bbi.postedby
        WHERE bulletinboardid=%s
        GROUP BY bbi.bulletinboardid
        ORDER by bbi.bulletinboardid DESC
        """ %pk
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
        return Response(result)

        # queryset = models.Bulletinboardinfo.objects.filter(pk=pk)[0]
        # serializer = adminserializers.BulletinboardlistinfoSerializer(queryset, many=False)
        # return Response(serializer.data)

    def destroy(self, request, pk=None):
        sql = """
        DELETE FROM bulletinmappinginfo 
        WHERE bulletinboardid=%s
        """ %pk
        cursor = connection.cursor()
        cursor.execute(sql)
        sql = """
        DELETE FROM bulletinboardinfo 
        WHERE bulletinboardid=%s
        """ %pk
        #print sql;
        aldata = {}
        aldata['pagename']       = 'bulletinboard'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a Announcement'
        add_activitylog(request, aldata)


        cursor = connection.cursor()
        cursor.execute(sql)

        return Response('"msg":"delete"')

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

        # aldata = {}
        # aldata['pagename']       = 'bulletinboard'
        # aldata['operation']      = 'Insert'
        # aldata['stringsentence'] = 'New Announcement created'
        # add_activitylog(request, aldata)
        # return Response(request.DATA)

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
        et.previoustext = unicode(prevtext)
        et.edittext     = unicode(modified)
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
        studentid               = request.GET.get('studentid');
        assignedid              = request.GET.get('assignedid');
        assignedtype            = request.GET.get('assignedtype');
        billboard.resourceid    = assignedid
        billboard.resourcetype  = str(assignedtype)
        billboard.studentid     = str(studentid)
        billboard.votescount    = 0
        billboard.lastvotedby   = 0
        billboard.postedby      = str(request.user.username)
        billboard.posteddate    = time.strftime('%Y-%m-%d %H:%M:%S')
        billboard.save()

        if assignedtype == "ar":
            sql = '''
            UPDATE assignresourceinfo
                SET isbillboard = 1
            WHERE assignedid = '%s' ''' % (assignedid)

        if assignedtype == "aw":
            sql = '''
            UPDATE assignwrittenworkinfo
                SET isbillboard = 1
            WHERE assignwrittenworkid = '%s' ''' % (assignedid)
            
        cursor = connection.cursor()
        cursor.execute(sql)        

        aldata = {}
        aldata['pagename']       = 'viewassignmentanswer'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'Resource Sent To NoticeBoard'
        add_activitylog(request, aldata)

        return Response('saved')

    def list(self, request):
        result = []
        sql = '''
        SELECT * FROM 
        ((
        SELECT bbi.billboardid as id,
            bbi.resourceid as assignedid,
            bbi.resourcetype as resourcetype,
            bbi.studentid as studentid,
            ri.resourceid as resourceid,
            ri.resourcetitle as title,
            concat(au.first_name,' ',au.last_name) as firstname,
            date(bbi.posteddate) as posteddate,
            (SELECT count(*) 
                FROM billboardratinginfo 
                WHERE billboardid=bbi.billboardid) 
            AS rating
        FROM billboardinfo bbi
        INNER JOIN assignresourceinfo ari ON ari.assignedid=bbi.resourceid
        INNER JOIN resourceinfo ri ON ri.resourceid=ari.resourceid
        INNER JOIN auth_user au ON au.username=bbi.studentid
        WHERE bbi.resourcetype = "ar"
        )
        UNION ALL
        (
        SELECT bbi.billboardid as id,  
            bbi.resourceid as assignedid,
            bbi.resourcetype as resourcetype,
            bbi.studentid as studentid,
            wwi.writtenworkid as resourceid,
            wwi.writtenworktitle as title,
            concat(au.first_name,' ',au.last_name) as firstname,
            date(bbi.posteddate) as posteddate,
            (SELECT count(*) 
                FROM billboardratinginfo 
                WHERE billboardid=bbi.billboardid)
            AS rating
        FROM billboardinfo bbi
        INNER JOIN assignwrittenworkinfo awwi ON awwi.assignwrittenworkid=bbi.resourceid
        INNER JOIN writtenworkinfo wwi ON wwi.writtenworkid=awwi.writtenworkid
        INNER JOIN auth_user au ON au.username=bbi.studentid
        WHERE bbi.resourcetype = "aw"
        )) as temp ORDER BY posteddate DESC
        '''
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

        return Response(result)

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
        
        if data.get('assignedtype') == "ar":
            arirm = models.Assignresourceinfo.objects.get(pk=pk)
            arirm.rubric_marks    = data.get('ans')
            arirm.rubric_n_mark   = data.get('ans_n')
            arirm.save()

        if data.get('assignedtype') == "aw":
            awirm = models.Assignwrittenworkinfo.objects.get(pk=pk)
            awirm.rubric_marks    = data.get('ans')
            awirm.rubric_n_mark   = data.get('ans_n')
            awirm.save()

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

    queryset = models.Stickyinfo.objects.filter().order_by('-createddate')
    serializer_class = adminserializers.StickyinfoSerializer

    def create(self, request):
        stickylist = models.Stickyinfo()
        stickydata =  json.loads(request.DATA.keys()[0])
        stickylist.title = stickydata.get('title')
        stickylist.isdeleted = 0
        stickylist.createdby = request.user.id
        stickylist.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        stickylist.save()

        aldata = {}
        aldata['pagename']       = 'sticky-notes-list'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New stickynotes Created'
        add_activitylog(request, aldata)

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

    def list(self, request):
        sql = '''
        SELECT  resource_id,
                resource_folder_id,
                resourcetype,
                resourcetitle,
                resourcedescription,
                fileurl,
                isdeleted,
                createddate
        FROM admin_resources 
        WHERE resource_folder_id=%s
        '''  % (request.GET.get('folderid'))
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
        admin.resource_folder_id = admindata.get('folderid')
        admin.fileurl = admindata.get('fileurl')
        admin.createdby = request.user.id
        admin.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        admin.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk):
        models.AdminResources.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

class ClassinfoViewSet(viewsets.ModelViewSet): 
    queryset = models.Classroominfo.objects.all()
    serializer_class = adminserializers.ClassroominfoSerializer

    def list(self, request):
        l =  request.user.groups.values_list('name',flat=True)[0]
        if l == 'Admin':
            wherecond = ""
        else:
            wherecond = "AND cri.schoolid='%s' AND cri.classid = '%s'"%(request.session.get('schoolid'),
                request.session.get('classid'))

        result = []

        sql = '''
        SELECT * FROM 
        ((
        SELECT cri.classroomid as id, 
            cri.resourceid as assignedid,
            cri.resourcetype,
            cri.studentid,
            ri.resourceid as resourceid,
            ri.resourcetitle as title,
            concat(au.first_name,' ',au.last_name) as firstname,
            date(cri.posteddate) as posteddate
        FROM classroominfo cri
        INNER JOIN assignresourceinfo ari ON ari.assignedid=cri.resourceid
        INNER JOIN resourceinfo ri ON ri.resourceid=ari.resourceid
        INNER JOIN auth_user au ON au.username=cri.studentid
        WHERE cri.resourcetype = "ar"
        %s
        )
        UNION ALL
        (
        SELECT cri.classroomid as id,
            cri.resourceid as assignedid,
            cri.resourcetype,
            cri.studentid,
            wwi.writtenworkid as resourceid,
            wwi.writtenworktitle as title,
            concat(au.first_name,' ',au.last_name) as firstname,
            date(cri.posteddate) as posteddate                
        FROM classroominfo cri
        INNER JOIN assignwrittenworkinfo awwi ON awwi.assignwrittenworkid=cri.resourceid
        INNER JOIN writtenworkinfo wwi ON wwi.writtenworkid=awwi.writtenworkid
        INNER JOIN auth_user au ON au.username=cri.studentid
        WHERE cri.resourcetype = "aw"
        %s
        )) as temp ORDER BY posteddate DESC
        '''% (wherecond, wherecond)
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

        return Response(result)

    def create(self, request):
        classroom = models.Classroominfo()
        classroomdata =  json.loads(request.DATA.keys()[0])
        classroom.resourceid            = classroomdata.get('assignedid')
        classroom.resourcetype          = str(classroomdata.get('assignedtype'))
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

        if classroomdata.get('assignedtype') == 'ar':
            sql = '''
            UPDATE assignresourceinfo
                SET isclassroom = 1
            WHERE assignedid = '%s' ''' % (classroomdata.get('assignedid'))

        if classroomdata.get('assignedtype') == 'aw':
            sql = '''
            UPDATE assignwrittenworkinfo
                SET isclassroom = 1
            WHERE assignwrittenworkid = '%s' ''' % (classroomdata.get('assignedid'))

        cursor = connection.cursor()
        cursor.execute(sql)
        
        aldata = {}
        aldata['pagename']       = 'viewassignmentanswer'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'Resource Sent To Classroom'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    def destroy(self, request, pk):
        models.Classroominfo.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

class StudentWrittenWork(viewsets.ModelViewSet):
    queryset = models.Assignwrittenworkinfo.objects.all()
    #serializer_class = adminserializers.MindmapSerializer

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        
        awwi = models.Assignwrittenworkinfo.objects.get(pk=pk)
        
        awwi.answertext = data.get('answertext')

        if data.get('originaltext'):
            awwi.originaltext = data.get('originaltext')

        if data.get('answerurl'):
            awwi.answerurl = data.get('answerurl')
            awwi.isrecord = 1

        if data.get('isanswered'):
            awwi.isanswered = data.get('isanswered')
            awwi.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')

        if data.get('issaved'):
            awwi.issaved = data.get('issaved')
        
        #print awwi

        awwi.save()

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
        ar.previoustext = unicode(orig)
        ar.edittext     = unicode(modified)
        ar.typeofresource = 0
        ar.isapproved   = 0
        ar.isrejected   = 0
        ar.editedby     = request.user.username
        ar.editeddate   = time.strftime('%Y-%m-%d %H:%M:%S')
        ar.usertype     = int(usertype)

        ar.save()

        return Response({'msg':True})

    def list(self, request):
        sql = '''
        SELECT awwi.assignwrittenworkid AS id,
               awwi.isrecord,
               awwi.answerurl,
               wwi.writtenworkid,
               wwi.writtenworktitle,
               date(assigneddate) as createddate,
               date(answereddate) as answereddate,
               awwi.studentid,
               awwi.isanswered,
               awwi.issaved
        FROM assignwrittenworkinfo awwi
        INNER JOIN writtenworkinfo wwi on wwi.writtenworkid = awwi.writtenworkid 
        WHERE awwi.studentid='%s'
        GROUP BY wwi.writtenworkid, awwi.answereddate
        ORDER BY awwi.assignwrittenworkid DESC''' % (request.user.username)
        cursor = connection.cursor()
        cursor.execute(sql)
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
               ari.issaved,
               ari.rubric_id,
               ari.rubric_marks,
               ari.rubric_n_mark
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
                ar.assigntext = unicode(assigntext)
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


class StudentAssignWrittenWork(viewsets.ModelViewSet):
    queryset = models.Assignwrittenworkinfo.objects.all()
    #serializer_class = adminserializers.MindmapSerializer

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        
        awwi = models.Assignwrittenworkinfo.objects.get(pk=pk)
        
        awwi.answertext = summer_decode(data.get('answertext'))

        if data.get('originaltext'):
            awwi.originaltext = summer_decode(data.get('originaltext'))

        if data.get('answerurl'):
            awwi.answerurl = data.get('answerurl')
            awwi.isrecord = 1

        if data.get('isanswered'):
            awwi.isanswered = data.get('isanswered')
            awwi.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')

        if data.get('issaved'):
            awwi.issaved = data.get('issaved')
        
        awwi.save()

        aldata = {}
        aldata['pagename']       = 'viewassignwrittenwork'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'Answered For Writtenwork'
        add_activitylog(request, aldata)

        # assignedid  = pk;
        
        # spanid      = data.get('spanid');
        # fulltext    = data.get('fulltext');
        # orig        = data.get('orig');
        # modified    = data.get('modified');
        # usertype    = data.get('type');
        # answertext  = data.get('answertext');

        # ar = models.Editingtext()
        # ar.editid       = int(assignedid)
        # ar.spanid       = str(spanid)
        # ar.previoustext = str(orig)
        # ar.edittext     = str(modified)
        # ar.typeofresource = 0
        # ar.isapproved   = 0
        # ar.isrejected   = 0
        # ar.editedby     = request.user.username
        # ar.editeddate   = time.strftime('%Y-%m-%d %H:%M:%S')
        # ar.usertype     = int(usertype)

        # ar.save()

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
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

    def retrieve(self, request, pk=None):
        sql = '''
        SELECT awwi.assignwrittenworkid AS id,
               awwi.isrecord,
               awwi.answerurl,
               wwi.writtenworkid,
               wwi.writtenworktitle,
               wwi.description,
               wwi.writtenimage,
               date(assigneddate) as createddate,
               date(answereddate) as answereddate,
               awwi.studentid,
               awwi.isanswered,
               awwi.issaved,
               awwi.rubric_id,
               awwi.rubric_marks,
               awwi.answertext,
               awwi.rubric_n_mark
        FROM assignwrittenworkinfo awwi
        INNER JOIN writtenworkinfo wwi on wwi.writtenworkid = awwi.writtenworkid 
        WHERE awwi.assignwrittenworkid='%s'
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
                ar.assigntext = unicode(assigntext)
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


class AssignedWrittenworkStudents(viewsets.ModelViewSet):
    queryset = models.Assignwrittenworkinfo.objects.all()
    #serializer_class = adminserializers.MindmapSerializer

    def retrieve(self, request, pk=None):
        studentcond = ''
        if request.GET.get('studentid'):
            studentcond = "AND awwi.studentid = '" + request.GET.get('studentid') + "'"

        sql = '''
        SELECT 
                awwi.assignwrittenworkid AS id,
                awwi.isrecord,
                awwi.answerurl,
                wwi.writtenworkid,
                wwi.writtenworktitle,
                wwi.description,
                wwi.writtenimage,
                date(assigneddate) as createddate,
                date(answereddate) as answereddate,
                awwi.studentid,
                awwi.isanswered,
                awwi.issaved,
                awwi.rubric_id,
                awwi.rubric_marks,
                awwi.answertext,
                awwi.rubric_n_mark,
                awwi.assignedby,
                au.first_name as firstname,
                au.last_name as lastname,
                awwi.originaltext,
                awwi.isbillboard,
                awwi.isclassroom
        FROM assignwrittenworkinfo awwi
        INNER JOIN writtenworkinfo wwi on wwi.writtenworkid = awwi.writtenworkid 
        INNER JOIN auth_user au on au.username = awwi.studentid 
        WHERE awwi.assignwrittenworkid=%s
              %s
        GROUP BY awwi.studentid
        ORDER BY assigneddate DESC''' % (pk, studentcond)

        cursor = connection.cursor()
        cursor.execute(sql)
        #print sql;
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)


class EditAnswerResourceViewSet(viewsets.ModelViewSet):
    queryset = models.Editingtext.objects.all()
    serializer_class = adminserializers.EditingtextSerializer

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
            AND isapproved = 1 ''' % (unicode(spanid))
        cursor = connection.cursor()
        cursor.execute(sql)
        result =  cursor.fetchone()
        if result:
            previoustext = result[0];
        # print "answertext --> " + answertext
        # print "previoustext --> " + previoustext
        # print "edittext --> " + edittext
        approvedanswertext = answertext.replace(previoustext,edittext)
        # print "approvedanswertext --> " + approvedanswertext

        #updating approved answer text
        sql = '''
        UPDATE assignresourceinfo 
           SET answertext = '%s'
           WHERE assignedid = '%s' ''' % (approvedanswertext.replace("'", '"'), assignedid)
        cursor = connection.cursor()
        cursor.execute(sql)

        #resetting the previous one if set
        sql = '''
        UPDATE editingtext
            SET isapproved = 0
        WHERE spanid = '%s' ''' % (unicode(spanid))
        cursor = connection.cursor()
        cursor.execute(sql)

        # #marking the selected as approved
        sql = '''
        UPDATE editingtext
            SET isapproved = 1,
            previoustext = '%s'
        WHERE editingid = '%s' ''' % (edittext.replace("'", '"'), pk)
        cursor = connection.cursor()
        cursor.execute(sql)

        return Response('approved')

class EditAnswerWrittenworkViewSet(viewsets.ModelViewSet):
    queryset = models.Editingtext.objects.all()
    serializer_class = adminserializers.EditingtextSerializer

    def retrieve(self, request, pk=None):
        import MySQLdb
        assignedid = request.GET.get('assignedid')
        sql = '''
        SELECT et.previoustext,
            et.edittext,
            awwi.answertext,
            et.spanid
        FROM editingtext et
        JOIN assignwrittenworkinfo awwi 
            ON awwi.assignwrittenworkid = et.editid   
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
            AND isapproved = 1 ''' % (unicode(spanid))
        cursor = connection.cursor()
        cursor.execute(sql)
        result =  cursor.fetchone()
        if result:
            previoustext = result[0];

        approvedanswertext = answertext.replace(previoustext,edittext)
        
        #updating approved answer text
        sql = '''
        UPDATE assignwrittenworkinfo 
           SET answertext = '%s'
           WHERE assignwrittenworkid = '%s' ''' % (approvedanswertext.replace("'", '"'), assignedid)
        cursor = connection.cursor()
        cursor.execute(sql)

        #resetting the previous one if set
        sql = '''
        UPDATE editingtext
            SET isapproved = 0
        WHERE spanid = '%s' ''' % (unicode(spanid))
        cursor = connection.cursor()
        cursor.execute(sql)

        # #marking the selected as approved
        sql = '''
        UPDATE editingtext
            SET isapproved = 1,
            previoustext = '%s'
        WHERE editingid = '%s' ''' % (edittext.replace("'", '"'), pk)
        cursor = connection.cursor()
        cursor.execute(sql)

        return Response('approved')

class PeerRubricsReviewViewSet(viewsets.ModelViewSet):

    queryset = models.PeerRubricsReview.objects.all()
    serializer_class = adminserializers.PeerRubricsReviewSerializer

    def create(self, request):
        prr = models.PeerRubricsReview()
        prrdata =  json.loads(request.DATA.keys()[0])

        prrdataarr = prrdata.get('ansarr')

        for idx, prrd in enumerate(prrdataarr):
            prr.resourceid  = prrdata.get('resourceid')
            prr.studentid   = prrdata.get('studentid')
            prr.evaluatedby = str(request.user.username)
            prr.row_no      = idx
            prr.row_mark    = prrd
            prr.max_mark    = prrdata.get('maxmark')
            prr.save()

        return Response('created');

    def list(self, request):
        resourceid  = request.GET.get('resourceid')
        studentid   = request.GET.get('studentid')
        rubricid    = request.GET.get('rubricid')
        result = {}
        sql = '''
        SELECT  temp.resourceid, 
                temp.studentid, 
                row_no, 
                rowmark, 
                avgmark, 
                rm.jdata
        FROM (
            SELECT  resourceid, 
                    studentid, 
                    row_no, 
                    round(avg(row_mark),1) AS rowmark, 
                    round(avg(max_mark)) AS avgmark
            FROM peer_rubrics_review
            WHERE resourceid = '%s'
            AND studentid = '%s'
            GROUP BY resourceid, studentid, row_no
        ) AS temp
        LEFT JOIN assignresourceinfo ari ON ari.resourceid = temp.resourceid 
            AND ari.studentid = temp.studentid
        RIGHT JOIN rubric_matrix rm ON rm.disp_order = temp.row_no 
            AND ari.rubric_id = rm.refno
        WHERE refno = '%s'
            AND rm.datatype = 'B' 
        ''' % (resourceid, str(studentid), rubricid)
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result['prrlist'] = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

        sql =  '''
            SELECT rubric_n_mark
            FROM  assignresourceinfo
            WHERE resourceid = '%s'
            AND studentid = '%s'
            ''' % (resourceid, str(studentid))
    
        cursor = connection.cursor()
        cursor.execute(sql)
        result['rnmark'] =  cursor.fetchone()

        return Response(result)


class AssignmindmapinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Assignmindmapinfo.objects.all()
    serializer_class = adminserializers.AssignmindmapinfoSerializer

    def list(self, request):
        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
            request.GET.get('tdate'))

        retrivemindmapcond = ''
        if request.GET.get('assignedid'):
            retrivemindmapcond = "AND assignedid = '%s'" % (request.GET.get('assignedid'))
            
        sql = '''
        SELECT ammi.assignedid AS id,
               ammi.mindmapid,
               mmi.title,
               ammi.assigntext,
               ammi.answertext,
               ammi.comment,
               ammi.mapdata,
               date(assigneddate) as createddate,
               date(answereddate) as answereddate,
               ammi.studentid,
               ammi.isanswered,
               ammi.issaved
        FROM assignmindmapinfo ammi
        INNER JOIN mindmap mmi on mmi.id = ammi.mindmapid 
        WHERE mmi.isdelete=0
              AND ammi.studentid='%s'
              AND ammi.IsDelete=0
              %s
              %s
        GROUP BY ammi.mindmapid, ammi.answereddate
        ORDER BY ammi.assignedid DESC''' % (request.user.username, datecond, retrivemindmapcond)

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        return Response(result)

    def create(self, request):
        assigndata =  json.loads(request.DATA.keys()[0])

        for s in assigndata.get('students'):
            assignmindmapinfo = models.Assignmindmapinfo()
            assignmindmapinfo.mindmapid     = assigndata.get('mindmapid')
            assignmindmapinfo.assigntext    = summer_decode(unicode(assigndata.get('assigntext')))
            assignmindmapinfo.mapdata       = summer_decode(unicode(assigndata.get('mapdata')))
            assignmindmapinfo.studentid     = str(s)
            assignmindmapinfo.isdelete      = 0
            assignmindmapinfo.issaved       = 0
            assignmindmapinfo.isanswered    = 0
            assignmindmapinfo.assignedby    = str(request.user.username)
            assignmindmapinfo.assigneddate  = time.strftime('%Y-%m-%d %H:%M:%S')
            assignmindmapinfo.answereddate  = time.strftime('%Y-%m-%d %H:%M:%S')
            assignmindmapinfo.save()

        return Response('"msg":"created"')

    # def retrieve(self, request, pk=None):
    #     queryset = models.Assignmindmapinfo.objects.get(pk=pk)
    #     serializer = adminserializers.AssignmindmapinfoSerializer(queryset, many=False)
    #     return Response(serializer.data)

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        ammi = models.Assignmindmapinfo.objects.get(pk=pk)
        ammi.answertext = summer_decode(unicode(data.get('answertext')))
        ammi.mapdata    = summer_decode(unicode(data.get('mapdata')))

        if data.get('isanswered'):
            ammi.isanswered = data.get('isanswered')
            ammi.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')

        if data.get('issaved'):
            ammi.issaved = data.get('issaved')
        
        ammi.save()

        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

class TeacherAssignedmindmapViewSet(viewsets.ModelViewSet):
    queryset = models.Assignmindmapinfo.objects.all()
    serializer_class = adminserializers.AssignmindmapinfoSerializer

    def list(self, request):
        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
            request.GET.get('tdate'))

        retrivemindmapcond = ''
        if request.GET.get('assignedid'):
            retrivemindmapcond = "AND assignedid = '%s'" % (request.GET.get('assignedid'))
            
        sql = '''
        SELECT ammi.assignedid AS id,
               ammi.mindmapid,
               mmi.title,
               ammi.assigntext,
               ammi.answertext,
               ammi.comment,
               ammi.mapdata,
               date(assigneddate) as createddate,
               date(answereddate) as answereddate,
               ammi.studentid,
               ammi.isanswered,
               ammi.issaved
        FROM assignmindmapinfo ammi
        INNER JOIN mindmap mmi on mmi.id = ammi.mindmapid 
        WHERE mmi.isdelete=0
              AND ammi.assignedby='%s'
              AND ammi.IsDelete=0
              %s
              %s
        GROUP BY ammi.mindmapid, ammi.assigneddate
        ORDER BY ammi.assignedid DESC''' % (request.user.username, datecond, retrivemindmapcond)

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        return Response(result)

    def retrieve(self, request, pk=None):

        sql = '''
        SELECT ammi.assignedid AS id,
               ammi.mindmapid,
               mmi.title,
               ammi.assigntext,
               ammi.answertext,
               ammi.comment,
               ammi.mapdata,
               date(assigneddate) as createddate,
               date(answereddate) as answereddate,
               ammi.studentid,
               ammi.isanswered,
               au.first_name as firstname,
               au.last_name as lastname,
               ammi.issaved
        FROM assignmindmapinfo ammi
        INNER JOIN mindmap mmi on mmi.id = ammi.mindmapid 
        INNER JOIN auth_user au on au.username = ammi.studentid 
        WHERE mmi.isdelete=0
              AND ammi.assignedby='%s'
              AND ammi.IsDelete=0
              AND ammi.mindmapid = %s
        GROUP BY ammi.studentid
        ORDER BY ammi.assignedid DESC''' % (request.user.username, pk)

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        ammi = models.Assignmindmapinfo.objects.get(pk=pk)
        ammi.comment = summer_decode(unicode(data.get('comment')))
        ammi.save()

        return Response('"msg":"update"')

class TopicInfoViewSet(viewsets.ModelViewSet):

    queryset = models.Topicinfo.objects .all()
    serializer_class = adminserializers.TopicsSerializer

    def treeify(self, flatlist, idAttr = 'postid', parentAttr = 'parentid', childrenAttr = 'comments'):

        treeList = [];
        lookup = {};
        for fl in flatlist:
            lookup[fl[idAttr]] = fl
            fl[childrenAttr] = []
        
        for fl in flatlist:
            try:
                lookup[fl[parentAttr]][childrenAttr].append(fl)
            except Exception as e:
                treeList.append(fl)
        return treeList

    def list(self, request):
        topicid = request.GET.get('topicid')
        topicname = request.GET.get('topicname')
        # if topicid :
        #     queryset = models.Topicinfo.objects.filter(topicid=topicid).order_by('-createddate')
        # else:
        #     queryset = models.Topicinfo.objects.filter().order_by('-createddate')
        #     serializer = adminserializers.TopicsSerializer(queryset, many=True)
        sql = '''
        SELECT  ti.topicid,
                ti.topicname,
                ti.topicdetails,
                ti.createddate,
                a.first_name AS username,
                (SELECT count(*) FROM postinfo WHERE topicid=ti.topicid) AS tot_comment
        FROM topicinfo ti
        LEFT JOIN auth_user a ON a.id = ti.createdby
        ORDER BY ti.createddate DESC
        '''
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

    def retrieve(self, request, pk=None):
        sql = '''
            SELECT ti.topicname,
                   ti.topicdetails,
                   ti.createddate,
                   a.first_name AS username
            FROM topicinfo ti
            LEFT JOIN auth_user a ON a.id = ti.createdby
            WHERE ti.topicid = '%s' ''' % (pk)
        cursor = connection.cursor()
        #print sql
        cursor.execute(sql)
        desc = cursor.description
        result = dict(zip([col[0] for col in desc], cursor.fetchone()))
        sql = '''
        SELECT   p.postid,
                   p.postdetails,
                   p.parentid,
                   p.posteddate,
                   p.parentid,
                   a.first_name AS postedby
            FROM postinfo p
            LEFT JOIN auth_user a ON a.id = p.postedby
            WHERE p.topicid = '%s' 
            ORDER BY p.posteddate DESC''' % (pk)

        cursor = connection.cursor()
        #print sql
        cursor.execute(sql)
        desc = cursor.description
        result_comment = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        result['comments'] = self.treeify(result_comment)
        return Response(result)
    
    def create(self, request):
        topics = models.Topicinfo()
        topicinfodata =  json.loads(request.DATA.keys()[0])
        topics.topicid = topicinfodata.get('topicid',0)
        topics.forumid = topicinfodata.get('forumid',0)
        topics.totalpost = topicinfodata.get('totalpost',0)
        topics.topicdetails = summer_decode(topicinfodata.get('topicdetails',0))
        topics.forumid = topicinfodata.get('forumid',0)
        topics.topicname = summer_decode(topicinfodata.get('topicname',0))
        topics.createdby = request.user.id
        topics.lastpostedby = request.user.id
        topics.username = request.user.get_full_name()
        topics.lastposteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        topics.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        topics.save()

        aldata = {}
        aldata['pagename']       = 'newtopic'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Forum Created'
        add_activitylog(request, aldata)

        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        models.Topicinfo.objects.get(pk=pk).delete()
        sql = """
        DELETE FROM postinfo 
        WHERE topicid=%s
        """ %pk
        cursor = connection.cursor()
        cursor.execute(sql)

        aldata = {}
        aldata['pagename']       = 'newtopic'
        aldata['operation']      = 'Delete'
        aldata['stringsentence'] = 'Deleted a Forum'
        add_activitylog(request, aldata)


        return Response('"msg":"delete"')

class PostinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Postinfo.objects.all()
    serializer_class = adminserializers.PostinfoSerializer

    def create(self, request):
        postinfo = models.Postinfo()
        postinfodata =  json.loads(request.DATA.keys()[0])
        postinfo.postid = postinfodata.get('postid')
        postinfo.topicid = postinfodata.get('topicid')
        postinfo.forumid = postinfodata.get('forumid',0)
        postinfo.parentid = postinfodata.get('parentid')
        postinfo.postdetails = postinfodata.get('postdetails',0)
        postinfo.postedby = request.user.id
        postinfo.posteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        postinfo.save()
        return Response(request.DATA)

class RubricImportViewSet(viewsets.ModelViewSet):

    queryset = models.RubricsHeader.objects.all().order_by('-slno')
    serializer_class = adminserializers.AdminrubricsSerializer

    def create(self, request):
        adminrubrics = models.RubricsHeader()
        rubricmatrix = models.RubricMatrix()
        rd = json.loads(request.DATA.keys()[0])

        import xlrd, os

        rd =  json.loads(request.DATA.keys()[0]);
        filepath = rd.get('filepath');
        fullpath = os.path.join('static/', filepath)
        book     = xlrd.open_workbook(fullpath)
        sheet    = book.sheet_by_index(0)
        columns  = int(sheet.ncols)
        rows     = int(sheet.nrows)
        
        adminrubrics.title       = rd.get('ttl')
        adminrubrics.description = rd.get('desc')
        adminrubrics.instruction = rd.get('instn')
        adminrubrics.teacher     = request.user.username
        adminrubrics.status      = 0
        adminrubrics.ts          = time.strftime('%Y-%m-%d %H:%M:%S')
        adminrubrics.save()
        
        refno = adminrubrics.slno

        headerdata = ''
        for hd in range(0, columns):
            headerdata += unicode(sheet.cell(0,hd).value)
            if (hd != columns-1) and (hd != 0):
                headerdata += "~~"

        rubricmatrix.refno      = refno
        rubricmatrix.datatype   = 'H'
        rubricmatrix.jdata      = unicode(headerdata)
        rubricmatrix.disp_order = 0
        rubricmatrix.save()

        for bdr in range(1, rows):
            bodydata = ''
            for bd in range(0, columns):
                bodydata += unicode(sheet.cell(bdr,bd).value)
                if bd != columns-1:
                    bodydata += "~~"
        
            rubricmatrix.refno      = refno
            rubricmatrix.datatype   = 'B'
            rubricmatrix.jdata      = unicode(bodydata)
            rubricmatrix.disp_order = bdr
            rubricmatrix.save()

        aldata = {}
        aldata['pagename']       = 'rubric_edit'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'Rubrics Imported'
        add_activitylog(request, aldata)

        return Response("msg")

class AssessmentInfoViewSet(viewsets.ModelViewSet):
    queryset = models.Assessmentinfo.objects.all()
    serializer_class = adminserializers.AssessmentinfoSerializer

    def list(self, request):
        queryset = models.Assessmentinfo.objects.filter(createdby=str(request.user.username)).order_by('-createddate')
        serializer = adminserializers.AssessmentinfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        assessment = models.Assessmentinfo()
        cdata =  json.loads(request.DATA.keys()[0])

        print cdata.get('title');
        print cdata.get('instruction');

        assessment.title        = summer_decode(cdata.get('title'))
        assessment.instruction  = summer_decode(cdata.get('instruction'))
        assessment.schoolid     = request.session.get('schoolid')
        assessment.classid      = request.session.get('classid')
        assessment.type         = str(cdata.get('type'))
        assessment.createdby    = str(request.user.username)
        assessment.createddate  = time.strftime('%Y-%m-%d %H:%M:%S')
        assessment.isdeleted    = 0
        assessment.save()
        return Response(request.DATA)

    def destroy(self, request, pk=None):
        models.Assessmentinfo.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

class AssignmentRatingViewSet(viewsets.ModelViewSet):
    queryset = models.Assignresourceinfo.objects.all()
    serializer_class = adminserializers.AssignresourceinfoSerializer

    def update(self, request, pk=None):
        rating = request.GET.get('rating')        
        # sql = '''
        # UPDATE assignwrittenworkinfo
        #     SET answerrating = '%s'
        # WHERE assignwrittenworkid = '%s' ''' % (rating,pk)
        sql = '''
        UPDATE assignresourceinfo
            SET answerrating = '%s'
        WHERE assignedid = '%s' ''' % (rating,pk)
        
        cursor = connection.cursor()
        cursor.execute(sql)
        return Response('"msg":"updated"')

class BillboardRatingViewSet(viewsets.ModelViewSet):
    queryset = models.Billboardratinginfo.objects.all()
    serializer_class = adminserializers.BillboardratinginfoSerializer

    def create(self, request):
        billboardrating = models.Billboardratinginfo()
        cdata =  json.loads(request.DATA.keys()[0])
        studentid                   = cdata.get('studentid');
        rating                      = cdata.get('rating');
        billboardid                 = cdata.get('billboardid');
        billboardrating.billboardid = billboardid
        billboardrating.rating      = rating
        billboardrating.studentid   = str(studentid)
        billboardrating.ratedby     = str(request.user.username)
        billboardrating.rateddate   = time.strftime('%Y-%m-%d %H:%M:%S')
        billboardrating.save()
        return Response(request.DATA)

    def list(self, request):
        billboardid = request.GET.get('billboardid')

        data = {}

        sql = """
        SELECT avg(rating) as rating
        FROM  billboardratinginfo
        WHERE  billboardid = '%s' 
        """ % (billboardid)

        cursor = connection.cursor()
        cursor.execute(sql)
        data['avgrating'] =  cursor.fetchone()[0]

        sql = """
        SELECT count(*) as rating
        FROM  billboardratinginfo
        WHERE  ratedby = '%s' 
        AND billboardid = '%s' 
        """ % (str(request.user.username),billboardid)

        cursor = connection.cursor()
        cursor.execute(sql)
        data['israted'] =  cursor.fetchone()[0]

        return Response(data)

class BillboardCommentViewSet(viewsets.ModelViewSet):
    queryset = models.Billboardcommentinfo.objects.all()
    serializer_class = adminserializers.BillboardcommentinfoSerializer

    def create(self, request):
        billboardcomment = models.Billboardcommentinfo()
        cdata =  json.loads(request.DATA.keys()[0])
        studentid                       = cdata.get('studentid');
        comment                         = cdata.get('comment');
        billboardid                     = cdata.get('billboardid');
        billboardcomment.billboardid    = billboardid
        billboardcomment.comment        = summer_decode(unicode(comment))
        billboardcomment.studentid      = str(studentid)
        billboardcomment.commentedby    = str(request.user.username)
        billboardcomment.commenteddate  = time.strftime('%Y-%m-%d %H:%M:%S')
        billboardcomment.save()
        return Response(request.DATA)

    def list(self, request):
        billboardid = request.GET.get('billboardid')

        sql = """
        SELECT bbci.*,
        concat(au.first_name,' ',au.last_name) as name 
        FROM billboardcommentinfo as bbci
        INNER JOIN auth_user au ON au.username=bbci.commentedby
        WHERE billboardid = '%s' 
        """ % (billboardid)

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

        return Response(result)

class RichmindmapViewSet(viewsets.ModelViewSet):
    queryset = models.Assignmindmapinfo.objects.all()
    serializer_class = adminserializers.RichmindmapSerializer

    def create(self, request):
        assignmindmapinfo = models.Assignmindmapinfo()
        assigndata =  json.loads(request.DATA.keys()[0])
        assignmindmapinfo.mapdata = assigndata.get('mapdata')
        assignmindmapinfo.assigntext = assigndata.get('assigntext','')
        assignmindmapinfo.mindmapid = 0
        assignmindmapinfo.isanswered = 0
        assignmindmapinfo.issaved = 0
        assignmindmapinfo.isdelete = 0
        assignmindmapinfo.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')
        assignmindmapinfo.assigneddate = time.strftime('%Y-%m-%d %H:%M:%S')
        assignmindmapinfo.save()
        return Response('"msg":"created"')

class studentwrittenworkViewSet(viewsets.ModelViewSet):
    queryset = models.Writtenworkinfo.objects.all()
    serializer_class = adminserializers.WrittenworkinfoSerializer

    def list(self, request):
        fieldcond=""
        if request.GET.get('writtenworkid'):
            fieldcond="AND wwi.writtenworkid=%s"%request.GET.get('writtenworkid')
        sql = '''
        SELECT  wwi.writtenworkid,
                wwi.writtenworktitle,
                awi.answertext,
                awi.isclassroom,
                date(awi.assigneddate) AS assigneddate,
                date(awi.publisheddate) AS publisheddate,
                wwi.description,
                au.first_name,
                au.last_name,
                date(awi.assigneddate) as assigneddate,
                awi.studentid 
        FROM writtenworkinfo wwi 
        INNER JOIN assignwrittenworkinfo awi ON awi.writtenworkid = wwi.writtenworkid
        INNER JOIN auth_user au ON au.username=awi.studentid 
        WHERE awi.studentid = '%s'
        %s
        ORDER BY wwi.createddate DESC
        ''' % (str(request.GET.get('studentid')),fieldcond)
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        return Response(result)

    def destroy(self, request, pk):
        models.Writtenworkinfo.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')


class MyProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Teacherinfo.objects.all()
    serializer_class = adminserializers.TeacherinfoSerializer
    def list(self, request):
        queryset = models.Teacherinfo.objects.filter(username=request.user.username)
        #print queryset;
        serializer = adminserializers.TeacherinfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        teacher = models.Teacherinfo.objects.get(username=pk)
        teacherdata =  json.loads(request.DATA.keys()[0])
        teacher.firstname = teacherdata.get('firstname')
        teacher.lastname = teacherdata.get('lastname','')
        teacher.password = teacherdata.get('password')
        teacher.emailid = teacherdata.get('emailid')
        teacher.imageurl = teacherdata.get('imageurl','')
        teacher.save()

        request.user.set_password(teacherdata.get('password'))
        request.user.full_name =teacherdata.get('firstname')
        request.user.save() 
        
        return Response('"msg":"updated"')

class AssessmentQAInfoViewSet(viewsets.ModelViewSet):
    queryset = models.AssessmentQAInfo.objects.all()
    serializer_class = adminserializers.AssessmentQAInfoSerializer

    def list(self, request):
        assessmentid = request.GET.get('assessmentid')
        queryset = models.AssessmentQAInfo.objects.filter(assessmentid=assessmentid).order_by('-id')
        serializer = adminserializers.AssessmentQAInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        assessmentqa = models.AssessmentQAInfo()
        aqadata =  json.loads(request.DATA.keys()[0])
        assessmentqa.assessmentid = aqadata.get('assessmentid')
        assessmentqa.question     = summer_decode(aqadata.get('question'))
        assessmentqa.answer       = aqadata.get('answer')
        assessmentqa.answeroption = aqadata.get('answeroption','')
        assessmentqa.actualmark   = aqadata.get('actualmark')
        assessmentqa.save()
        return Response(request.DATA)

    def destroy(self, request, pk=None):
        models.AssessmentQAInfo.objects.get(pk=pk).delete()
        return Response('"msg":"delete"')

class StudentAssignAssessment(viewsets.ModelViewSet):
    queryset = models.Assignassessmentinfo.objects.all()
    serializer_class = adminserializers.AssignassessmentinfoSerializer

    def list(self, request):

        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))
        sql = '''
        SELECT assignedid AS id,
               ai.id as assessmentid,
               ai.title,
               date(assigneddate) as createddate,
               aai.studentid,
               aai.isanswered,
               aai.issaved
        FROM assignassessmentinfo aai
        INNER JOIN assessmentinfo ai on ai.id = aai.assessmentid 
        WHERE aai.assignedby='%s'
              %s
        GROUP BY aai.assessmentid, aai.assigneddate
        ORDER BY aai.assignedid DESC''' % (request.user.username, datecond)


        cursor = connection.cursor()
        cursor.execute(sql)
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
               ari.assigntext,
               ari.studentid,
               ari.isanswered,
               ari.issaved,
               ari.rubric_id,
               ari.rubric_marks,
               ari.rubric_n_mark
        FROM assignresourceinfo ari
        INNER JOIN  resourceinfo ri on ri.resourceid = ari.resourceid 
        WHERE assignedid = %s
        ''' % pk
        cursor = connection.cursor()
        cursor.execute(sql)
       # print sql
        result = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
        #print result
        return Response(result)

    def create(self, request):
        data = json.loads(dict(request.DATA).keys()[0]);
        students    = data.get('students');
        assessmentid= data.get('assessmentid');
        enddate     = data.get('enddate');
        note        = summer_decode(data.get('note'));

        for s in students:
            sql = """
            DELETE FROM assignassessmentinfo 
            WHERE assessmentid='%s'
            AND studentid='%s'
            """ % (int(assessmentid),str(s))

            cursor = connection.cursor()
            cursor.execute(sql)

            ar = models.Assignassessmentinfo()
            ar.studentid     = str(s)
            ar.assessmentid  = int(assessmentid)
            ar.note          = str(note)
            ar.isanswered    = 0
            ar.issaved       = 0
            ar.isbillboard   = 0
            ar.isclassroom   = 0
            ar.enddate       = enddate
            ar.assignedby    = str(request.user.username)
            ar.assigneddate  = time.strftime('%Y-%m-%d %H:%M:%S')
            ar.answereddate  = time.strftime('%Y-%m-%d %H:%M:%S')
            ar.totalmarks    = 0
            totalactualmarks = 0
            ar.studentid    = str(s)
            ar.assessmentid = int(assessmentid)
            ar.note         = str(note)
            ar.isanswered   = 0
            ar.issaved      = 0
            ar.isbillboard  = 0
            ar.isclassroom  = 0
            ar.enddate      = enddate
            ar.assignedby   = str(request.user.username)
            ar.assigneddate = time.strftime('%Y-%m-%d %H:%M:%S')
            ar.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')
            ar.totalmarks      = 0
            ar.totalactualmarks= 0
            ar.save()   

        aldata = {}
        aldata['pagename']       = 'assignassessment'
        aldata['operation']      = 'insert'
        aldata['stringsentence'] = 'New assessment assigned to students'
        add_activitylog(request, aldata)

        return Response(request.DATA)        

    def update(self, request, pk=None):

        data = {k:v[0] for k, v in dict(request.DATA).items()}
        
        ari = models.Assignresourceinfo.objects.get(pk=pk)
        
        ari.answertext = summer_decode(unicode(data.get('answertext')))

        if data.get('originaltext'):
            ari.originaltext = summer_decode(unicode(data.get('originaltext')))

        if data.get('answerurl'):
            ari.answerurl = unicode(data.get('answerurl'))
            ari.isrecord = 1

        if data.get('isanswered'):
            ari.isanswered = data.get('isanswered')
            ari.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')

        if data.get('issaved'):
            ari.issaved = data.get('issaved')
        
        ari.save()
        if data.get('spanid'):
            assignedid  = pk;
            spanid      = summer_decode(data.get('spanid'));
            fulltext    = summer_decode(data.get('fulltext'));
            orig        = summer_decode(data.get('orig'));
            modified    = summer_decode(data.get('modified'));
            usertype    = data.get('type');
            answertext  = summer_decode(data.get('answertext'));

            ar = models.Editingtext()
            ar.editid       = int(assignedid)
            ar.spanid       = unicode(spanid)
            ar.previoustext = unicode(orig)
            ar.edittext     = unicode(modified)
            ar.typeofresource = 0
            ar.isapproved   = 0
            ar.isrejected   = 0
            ar.editedby     = request.user.username
            ar.editeddate   = time.strftime('%Y-%m-%d %H:%M:%S')
            ar.usertype     = int(usertype)

            ar.save()

        aldata = {}
        aldata['pagename']       = 'viewassignresource'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'Answered For Resource'
        add_activitylog(request, aldata)

        return Response({'msg':True})

class ActivitylogInfoViewSet(viewsets.ModelViewSet):
    queryset = models.Activitylog.objects.all()
    serializer_class = adminserializers.ActivityloginfoSerializer

    def list(self, request):
        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (updateddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))
        sql = '''
        SELECT  loginid,
                pagename,
                operation,
                usertype,
                stringsentence,
                updateddate
        FROM activitylog 
        WHERE loginid = '%s'
        %s
        ORDER BY updateddate DESC
        ''' % (request.GET.get('studentid'),datecond)
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)


class ActivityassignmentInfoViewSet(viewsets.ModelViewSet):
    queryset = models.Assignresourceinfo.objects.all()
    serializer_class = adminserializers.ActivityassignmentinfoSerializer

    def list(self, request):
        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (ari.assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))
        sql = '''
        SELECT  ri.resourceid,
                ri.resourcetitle, 
                date(ari.assigneddate) as assigneddate, 
                cast(ari.answerrating as decimal(10,2)) AS rating,
                date(ari.answereddate) answereddate  
        FROM assignresourceinfo ari
        INNER JOIN resourceinfo ri ON ri.resourceid = ari.resourceid 
        WHERE ari.studentid ='%s'  
        AND ari.isanswered =1 
        %s 
        GROUP BY ari.resourceid,ari.answereddate DESC
        ORDER BY ri.resourceid 
        ''' % (request.GET.get('studentid'),datecond)
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

class ActivityassessmentInfoViewSet(viewsets.ModelViewSet):
    queryset = models.Assessmentlist.objects.all()
    serializer_class = adminserializers.ActivityassignmentinfoSerializer

    def list(self, request):
        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "WHERE (aai.assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))
        sql = '''
        SELECT  al.assessmenttitle,
                floor(avg(aa.rating)) as rating,
                date(aai .assigneddate) as assigneddate,
                date(aa.answereddate) as answereddate  
        FROM assessmentlist al
        INNER JOIN assignassessmentinfo aai on aai.assessmentid = al.assessmentid 
        INNER JOIN assessmentanswers aa on aa.assessmentid = al.assessmentid 
        %s
        GROUP BY al.assessmentid 
        ORDER BY al.assessmentid 
        ''' % (datecond)
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

class StudentassignedresourceInfoViewSet(viewsets.ModelViewSet):
    queryset = models.Assignresourceinfo.objects.all()
    #serializer_class = adminserializers.StudentassignedresourceInfoSerializer

    def retrieve(self, request, pk=None):
        studentcond = ''
        if request.GET.get('studentid'):
            studentcond = "AND ari.studentid = '" + request.GET.get('studentid') + "'"

        sql = '''
        SELECT 
                ari.assignedid AS id,
                ari.isrecord,
                ari.answerurl,
                ri.resourceid,
                ri.resourcetitle,
                ri.resourcedescription,
                date(assigneddate) as createddate,
                date(answereddate) as answereddate,
                ari.studentid,
                ari.isanswered,
                ari.issaved,
                ari.rubric_id,
                ari.rubric_marks,
                ari.answertext,
                ari.rubric_n_mark,
                ari.assignedby,
                au.first_name as firstname,
                au.last_name as lastname,
                ari.originaltext,
                ari.isbillboard,
                ari.isclassroom
        FROM assignresourceinfo ari
        INNER JOIN resourceinfo ri on ri.resourceid = ari.resourceid 
        INNER JOIN auth_user au on au.username = ari.studentid 
        WHERE ari.resourceid=%s
        %s
        GROUP BY ari.studentid
        ORDER BY assigneddate DESC
        ''' % (pk, studentcond)

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

class studentAssessmentInfoViewSet(viewsets.ModelViewSet):
    queryset = models.Assignassessmentinfo.objects.all()
    serializer_class = adminserializers.AssignassessmentinfoSerializer

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        aai = models.Assignassessmentinfo.objects.get(pk=pk)
        aaidata =  json.loads(request.DATA.keys()[0])
        
        if aaidata.get('issaved'):
            aai.issaved = aaidata.get('issaved')

        if aaidata.get('isanswered'):
            aai.isanswered = aaidata.get('isanswered')

        aai.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')
        aai.save()

        if aaidata.get('alreadysaved'):
            sql = """
                DELETE FROM assignassessmentqainfo 
                WHERE assessmentid='%s'
                """ % (int(pk))

            cursor = connection.cursor()
            cursor.execute(sql)
        sql=''
        result=''
        print(aaidata.get('aqaidanswer'))
        for k, v in dict(aaidata.get('aqaidanswer')).items():
            sql= '''
            SELECT actualmark,
                answer
            FROM assessmentqa
            WHERE id = '%s'           
            '''%(int(k))
            cursor = connection.cursor()
            cursor.execute(sql)
            result =  cursor.fetchone()
           
            aaid = models.AssignAssessmentQAInfo()
            aaid.assessmentqaid     = int(k)
            aaid.assessmentid       = int(aaidata.get('assessmentid'))
            aaid.assignassessmentid = int(pk)
            aaid.answer             = str(v)
            if result[1]==str(v):
                aaid.obtainedmark   = int(result[0])
            else:
                aaid.obtainedmark   = 0
            aaid.save()

        sql = '''
        SELECT SUM(aaqi.obtainedmark) AS totalobtainedmark,
            SUM(aqa.actualmark) AS totalactualmark 
        FROM assessmentqa aqa
        INNER JOIN assignassessmentqainfo aaqi ON aaqi.assessmentqaid=aqa.id
        WHERE aaqi.assignassessmentid = '%s'
        GROUP BY aaqi.assignassessmentid 
        '''%(int(pk))
        cursor = connection.cursor()
        cursor.execute(sql)
        result =  cursor.fetchone()
        aai = models.Assignassessmentinfo.objects.get(pk=pk)
        aai.totalmarks     = int(result[0])
        aai.totalactualmarks       = int(result[1])
        aai.save()
            

        aldata = {}
        aldata['pagename']       = 'viewassignresource'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'Answered For Resource'
        add_activitylog(request, aldata)

        return Response({'msg':True})

    def list(self, request):

        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))
        sql = '''
        SELECT assignedid AS id,
               ai.id as assessmentid,
               ai.title,
               ai.type,
               ai.createddate,
               aai.assigneddate,
               aai.answereddate,
               aai.studentid,
               aai.isanswered,
               aai.issaved
        FROM assignassessmentinfo aai
        INNER JOIN assessmentinfo ai on ai.id = aai.assessmentid 
        WHERE aai.studentid='%s'
              %s
        GROUP BY aai.assessmentid, aai.assigneddate
        ORDER BY aai.assignedid DESC''' % (request.user.username, datecond)
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

    def retrieve(self, request, pk=None):
        
        sql = '''
        SELECT assignedid AS id,
               ai.id as assessmentid,
               aqa.id as assessmentqaid,
               ai.title,
               aaqai.answer,
               ai.type,
               ai.instruction,
               aai.note,
               aqa.question,
               aqa.answeroption,
               aqa.actualmark,
               assigneddate as createddate,
               aai.studentid,
               aai.isanswered,
               aai.issaved
        FROM assignassessmentinfo aai
        INNER JOIN assessmentinfo ai on ai.id = aai.assessmentid 
        INNER JOIN assessmentqa aqa on aqa.assessmentid = aai.assessmentid 
        LEFT JOIN assignassessmentqainfo aaqai on aaqai.assessmentqaid = aqa.id
        WHERE aai.studentid='%s' AND aai.assignedid='%s'
        GROUP BY aqa.id, aai.assigneddate
        ORDER BY aai.assignedid DESC''' % (request.user.username, pk)

        #print sql

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        cursor = connection.cursor()
        cursor.execute(sql)

        return Response(result)

    def create(self, request):
        data = json.loads(dict(request.DATA).keys()[0]);
        students = data.get('students');
        resource = data.get('resource');
        rubricid = data.get('rubricid');
        assigntext = summer_decode(data.get('assigntext'));

        for r in resource:
            for s in students:
                
                sql = """
                DELETE FROM assignresourceinfo 
                WHERE studentid='%s'
                AND resourceid='%s'
                """ % (str(s),int(r))

                cursor = connection.cursor()
                cursor.execute(sql)

                ar = models.Assignresourceinfo()
                ar.resourceid = int(r)
                ar.studentid = str(s)
                ar.assigntext = unicode(assigntext)
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
        

        aldata = {}
        aldata['pagename']       = 'assignchapter'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New Resource Assigned to students'
        add_activitylog(request, aldata)

        return Response(request.DATA)

class AssessmentstatisticsInfo(viewsets.ModelViewSet):
    queryset = models.Assignassessmentinfo.objects.all()
    serializer_class = adminserializers.AssignassessmentinfoSerializer

    def list(self, request):
        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (ai.createddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))

        sql = '''
        SELECT  aai.assessmentid,
                ai.title,
                aai.assigneddate,
                aai.answereddate,
                aai.totalmarks,
                aai.totalactualmarks
        FROM assignassessmentinfo aai
        INNER JOIN assessmentinfo ai ON ai.id=aai.assessmentid
        WHERE aai.studentid='%s'
        %s
        ''' %(request.GET.get('studentid'), datecond)
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

class StatisticsstudentInfo(viewsets.ModelViewSet):
    queryset = models.Studentinfo.objects.filter(isdelete=0)
    serializer_class = adminserializers.StudentinfoSerializer
    
    def retrieve(self, request, pk=None):
        sql = '''
        SELECT  studentid,
                CONCAT(firstname,' ',lastname) AS name
        FROM studentinfo
        WHERE  username = '%s'
        ''' % pk
        cursor = connection.cursor()
        cursor.execute(sql)
        result = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
        return Response(result)

class ViewassignassessmentInfo(viewsets.ModelViewSet):
    queryset = models.Assignassessmentinfo.objects.all()
    serializer_class = adminserializers.AssignassessmentinfoSerializer
    
    def list(self, request):
        sql = '''
        SELECT  aai.assessmentid,
                aai.studentid,
                aai.enddate,
                aai.assignedby,
                aai.note,
                aai.answereddate,
                aai.totalmarks,
                aai.totalactualmarks,
                aai.isanswered,
                aai.issaved,
                au.first_name AS firstname,
                au.last_name AS lastname,
                ai.type
        FROM assignassessmentinfo aai
        INNER JOIN assessmentinfo ai ON aai.assessmentid = ai.id
        INNER JOIN auth_user au ON au.username=aai.studentid 
        WHERE assessmentid=%s
        ''' % request.GET.get('assessmentid')
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        return Response(result)

    def retrieve(self, request, pk=None):
        studentid=""
        if request.GET.get('studentid'):
            studentid="AND aai.studentid='%s'" % request.GET.get('studentid')
        sql='''
        SELECT assignedid AS id,
               aaqai.id AS assignqaid,
               ai.id as assessmentid,
               aqa.id as assessmentqaid,
               ai.title,
               aaqai.answer,
               ai.type,
               ai.instruction,
               aai.note,
               aqa.question,
               aqa.answeroption,
               aqa.actualmark,
               assigneddate as createddate,
               aai.studentid,
               aai.isanswered,
               aai.issaved,
               aai.totalmarks,
               aai.totalactualmarks
        FROM assignassessmentinfo aai
        INNER JOIN assessmentinfo ai on ai.id = aai.assessmentid 
        INNER JOIN assessmentqa aqa on aqa.assessmentid = aai.assessmentid 
        LEFT JOIN assignassessmentqainfo aaqai on aaqai.assessmentqaid = aqa.id
        WHERE aai.assessmentid='%s'
        %s
        GROUP BY aqa.id, aai.assigneddate
        ORDER BY aai.assignedid DESC
        '''%(pk, studentid)

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

class MindmapinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Mindmaplistinfo.objects.filter().order_by('-createddate')
    serializer_class = adminserializers.MindmaplistSerializer

    def create(self, request):
        mindmaplist = models.Mindmaplistinfo()
        mindmapdata =  json.loads(request.DATA.keys()[0])
        mindmaplist.title = mindmapdata.get('title')
        mindmaplist.isdeleted = 0
        mindmaplist.createdby = request.user.id
        mindmaplist.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        mindmaplist.save()

        aldata = {}
        aldata['pagename']       = 'mindmaplist'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'New stickynotes Created'
        add_activitylog(request, aldata)

        return Response(request.DATA)

class studentopenendedInfoViewSet(viewsets.ModelViewSet):
    queryset = models.Assignassessmentinfo.objects.all()
    serializer_class = adminserializers.AssignassessmentinfoSerializer

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        aai = models.Assignassessmentinfo.objects.get(pk=pk)
        aaidata =  json.loads(request.DATA.keys()[0])
        
        if aaidata.get('issaved'):
            aai.issaved = aaidata.get('issaved')

        if aaidata.get('isanswered'):
            aai.isanswered = aaidata.get('isanswered')

        aai.answereddate = time.strftime('%Y-%m-%d %H:%M:%S')
        aai.save()

        if aaidata.get('alreadysaved'):
            sql = """
                DELETE FROM assignassessmentqainfo 
                WHERE assignassessmentid='%s'
                """ % (int(pk))

            cursor = connection.cursor()
            cursor.execute(sql)
        sql=''
        result=''

        for k, v in dict(aaidata.get('aqaidanswer')).items():
            sql= '''
            SELECT actualmark,
                answer
            FROM assessmentqa
            WHERE id = '%s'           
            '''%(int(k))
            cursor = connection.cursor()
            cursor.execute(sql)
            result =  cursor.fetchone()
           
            aaid = models.AssignAssessmentQAInfo()
            aaid.assessmentqaid     = int(k)
            aaid.assessmentid       = int(aaidata.get('assessmentid'))
            aaid.assignassessmentid = int(pk)
            aaid.answer             = str(v)
            if result[1] == str(v):
                aaid.obtainedmark   = int(result[0])
            else:
                aaid.obtainedmark   = 0
            aaid.save()

        sql = '''
        SELECT SUM(aaqi.obtainedmark) AS totalobtainedmark,
            SUM(aqa.actualmark) AS totalactualmark 
        FROM assessmentqa aqa
        INNER JOIN assignassessmentqainfo aaqi ON aaqi.assessmentqaid=aqa.id
        WHERE aaqi.assignassessmentid = '%s'
        GROUP BY aaqi.assignassessmentid 
        '''%(int(pk))
        cursor = connection.cursor()
        cursor.execute(sql)
        result =  cursor.fetchone()
        aai = models.Assignassessmentinfo.objects.get(pk=pk)
        aai.totalmarks     = int(result[0])
        aai.totalactualmarks       = int(result[1])
        aai.save()
            

        aldata = {}
        aldata['pagename']       = 'viewassignresource'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'Answered For Resource'
        add_activitylog(request, aldata)

        return Response({'msg':True})

    def list(self, request):

        datecond = ''
        if request.GET.get('fdate') and request.GET.get('tdate'):
            datecond = "AND (assigneddate BETWEEN '{0} 00:00:00' AND '{1} 23:59:59')".format(request.GET.get('fdate'),
                request.GET.get('tdate'))
        sql = '''
        SELECT assignedid AS id,
               ai.id as assessmentid,
               ai.title,
               ai.type,
               ai.createddate,
               aai.assigneddate,
               aai.answereddate,
               aai.studentid,
               aai.isanswered,
               aai.issaved
        FROM assignassessmentinfo aai
        INNER JOIN assessmentinfo ai on ai.id = aai.assessmentid 
        WHERE aai.studentid='%s'
              %s
        GROUP BY aai.assessmentid, aai.assigneddate
        ORDER BY aai.assignedid DESC''' % (request.user.username, datecond)
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

    def retrieve(self, request, pk=None):
        
        sql = '''
        SELECT assignedid AS id,
               ai.id as assessmentid,
               aqa.id as assessmentqaid,
               ai.title,
               aaqai.answer,
               ai.type,
               ai.instruction,
               aai.note,
               aqa.question,
               aqa.answeroption,
               aqa.actualmark,
               assigneddate as createddate,
               aai.studentid,
               aai.isanswered,
               aai.issaved
        FROM assignassessmentinfo aai
        INNER JOIN assessmentinfo ai on ai.id = aai.assessmentid 
        INNER JOIN assessmentqa aqa on aqa.assessmentid = aai.assessmentid 
        LEFT JOIN assignassessmentqainfo aaqai on aaqai.assessmentqaid = aqa.id
        WHERE aai.studentid='%s' AND aai.assignedid='%s'
        GROUP BY aqa.id, aai.assigneddate
        ORDER BY aai.assignedid DESC''' % (request.user.username, pk)

        #print sql

        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        cursor = connection.cursor()
        cursor.execute(sql)

        return Response(result)

class teacherAssessmentInfoViewSet(viewsets.ModelViewSet):
    queryset = models.AssignAssessmentQAInfo.objects.all()
    serializer_class = adminserializers.AssignassessmentinfoSerializer

    def update(self, request, pk=None):
        data = {k:v[0] for k, v in dict(request.DATA).items()}
        # aai = models.Assignassessmentinfo.objects.get(pk=pk)
        aaidata =  json.loads(request.DATA.keys()[0])

        for k, v in dict(aaidata.get('obtainmark')).items():
            aai = models.AssignAssessmentQAInfo.objects.get(pk=k)
            aai.obtainedmark     = int(v)
            aai.save()

        aldata = {}
        aldata['pagename']       = 'viewassopenendedanswer'
        aldata['operation']      = 'Insert'
        aldata['stringsentence'] = 'Answer mark addedd'
        add_activitylog(request, aldata)

        return Response({'msg':True})

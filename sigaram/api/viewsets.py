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
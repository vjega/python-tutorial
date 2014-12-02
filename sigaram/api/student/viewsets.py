from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers

from portaladmin import models
import  studentserializers

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

class ResourceinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Resourceinfo.objects.all()
    serializer_class = studentserializers.ResourceinfoSerializer
    
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
        serializer = studentserializers.ResourceinfoSerializer(queryset, many=True)
        return Response(serializer.data)

class WrittenworkinfoViewSet(viewsets.ModelViewSet):
    queryset = models.Writtenworkinfo.objects.all()
    serializer_class = studentserializers.WrittenworkinfoSerializer

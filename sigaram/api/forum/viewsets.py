from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers

from portalaforum import models
import studentserializers
import json, time



class StudentnotesinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Notesinfo.objects.all()
    serializer_class = studentserializers.StudentnotesinfoSerializer

    def list(self, request):
        userid =  request.user.id
        if userid :
            queryset = models.Notesinfo.objects.filter(createdby=userid)
        else:
            queryset = models.Notesinfo.objects.all()
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
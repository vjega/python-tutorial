from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers

from portaladmin import models
import forumserializers
import json, time

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




class ForuminfoViewSet(viewsets.ModelViewSet):

    queryset = models.Foruminfo.objects.all()
    serializer_class = forumserializers.ForuminfoSerializer

    def create(self, request):
        foruminfo = models.Foruminfo()
        forumdata =  json.loads(request.DATA.keys()[0])
        foruminfo.forumid = forumdata.get('forumid')
        foruminfo.forumname = forumdata.get('forumname')
        foruminfo.totaltopic = forumdata.get('totaltopic',0)
        foruminfo.totalpost = forumdata.get('totalpost',0)
        foruminfo.createdby = request.user.id
        foruminfo.lastpostedby = forumdata.get('lastpostedby',0)
        foruminfo.lastposteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        foruminfo.isdelete = 0
        foruminfo.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        foruminfo.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

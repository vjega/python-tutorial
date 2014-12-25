from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from django.db import connection

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
        foruminfo.forumid = forumdata.get('forumid',0)
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


class TopicinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Topicinfo.objects.all()
    serializer_class = forumserializers.TopicinfoSerializer

    def list(self, request):
        forumid = request.GET.get('forumid')
        forumname = request.GET.get('forumname')
        sql = """
        SELECT topicid,
                forumid,
                topicname,
                totalpost,
                date(lastposteddate) as lastposteddate,
                firstname,
                totalpost 
        FROM topicinfo ti 
        LEFT OUTER JOIN logininfo li ON li.loginid = ti.lastpostedby 
        WHERE ti.forumid=%s
        ORDER BY topicid """ % forumid
        cursor = connection.cursor()
        #print sql
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)
    def create(self, request):
        topicinfo = models.Topicinfo()
        topicinfodata =  json.loads(request.DATA.keys()[0])
        topicinfo.topicid = topicinfodata.get('topicid',0)
        topicinfo.forumid = topicinfodata.get('forumid',0)
        topicinfo.topicname = topicinfodata.get('topicname',0)
        topicinfo.totaltopic = topicinfodata.get('totaltopic',0)
        topicinfo.totalpost = topicinfodata.get('totalpost',0)
        topicinfo.createdby = request.user.id
        topicinfo.lastpostedby = topicinfodata.get('lastpostedby',0)
        topicinfo.lastposteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        topicinfo.createddate = time.strftime('%Y-%m-%d %H:%M:%S')
        topicinfo.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')


class PostreplyinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Postreplyinfo.objects.all()
    serializer_class = forumserializers.PostreplyinfoSerializer

    def create(self, request):
        postreplyinfo = models.Postreplyinfo()
        postreplydata =  json.loads(request.DATA.keys()[0])
        print '^'*80
        print postreplydata
        print request.DATA
        postreplyinfo.postreplyid = postreplydata.get('postreplyid',0)
        postreplyinfo.postid = postreplydata.get('topicid',0)
        postreplyinfo.postdetails = postreplydata.get('postdetails',0)
        postreplyinfo.postedby = postreplydata.get('postedby',0)
        postreplyinfo.posteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        postreplyinfo.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')


class PostinfoViewSet(viewsets.ModelViewSet):

    queryset = models.Postinfo.objects.all()
    serializer_class = forumserializers.PostinfoSerializer
    def list(self, request):
        postid = request.GET.get('postid')
        topicid = request.GET.get('topicid')
        forumid = request.GET.get('forumid')
        sql = """
        SELECT  postid,
                topicid,
                forumid,
                postdetails,
                date(posteddate) as posteddate,
                firstname 
        FROM postinfo pf
        left outer join logininfo lf on lf.loginid = pf.postedby 
        where pf.topicid=%s
        order by postid  """ % topicid

        cursor = connection.cursor()
        #print sql
        cursor.execute(sql)
        desc = cursor.description
        result =  [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        return Response(result)

    def create(self, request):
        postinfo = models.Postinfo()
        postinfodata =  json.loads(request.DATA.keys()[0])
        postinfo.postid = postinfodata.get('postid',0)
        postinfo.topicid = postinfodata.get('topicid',0)
        postinfo.forumid = postinfodata.get('forumid',0)
        postinfo.postdetails = postinfodata.get('postdetails',0)
        postinfo.postedby = postinfodata.get('postedby',0)
        postinfo.posteddate = time.strftime('%Y-%m-%d %H:%M:%S')
        postinfo.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')


class ActivitylogViewSet(viewsets.ModelViewSet):

    queryset = models.Activitylog.objects.all()
    serializer_class = forumserializers.ActivitylogSerializer

    def create(self, request):
        activitylog = models.Activitylog()
        activitylogdata =  json.loads(request.DATA.keys()[0])
        activitylog.activityid = activitylogdata.get('activityid')
        activitylog.loginid = activitylogdata.get('loginid')
        activitylog.pagename = activitylogdata.get('pagename')
        activitylog.operation = activitylogdata.get('operation',0)
        activitylog.usertype = activitylogdata.get('usertype',0)
        activitylog.stringsentence = activitylogdata.get('stringsentence',0)
        activitylog.updateddate = time.strftime('%Y-%m-%d %H:%M:%S')
        activitylog.save()
        return Response(request.DATA)

    def update(self, request, pk=None):
        return Response('"msg":"update"')

    def destroy(self, request, pk=None):
        return Response('"msg":"delete"')

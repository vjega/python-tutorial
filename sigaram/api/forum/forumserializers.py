from rest_framework import serializers
from portaladmin import models

class ForuminfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Foruminfo
        fields = ('forumid',  'forumname','totaltopic',
                  'totalpost','createdby', 'createddate',
                  'lastpostedby','lastposteddate','isdelete')

class TopicinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Topicinfo
        fields = ('topicid',  'forumid','topicname','topicdetails',
                  'totalpost','createdby', 'createddate',
                  'lastpostedby','lastposteddate')

class PostreplyinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Postreplyinfo
        fields = ('postreplyid',  'postid','postdetails',
                  'postedby','posteddate')
        
class PostinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Postinfo
        fields = ('postid',  'topicid','forumid',
                  'postdetails','postedby','posteddate')

# class ActivitylogSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.Activitylog
#         fields = ('activityid',  'loginid','pagename',
#                   'operation','usertype','stringsentence','updateddate')
        

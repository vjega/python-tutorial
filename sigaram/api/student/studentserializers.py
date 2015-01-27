from rest_framework import serializers
from portaladmin import models

class StudentinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Studentinfo
        fields = ('studentid',  'username',
                  'firstname','lastname', 'emailid',
                  'imageurl','schoolid','classid')
        
class ResourceinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Resourceinfo
        fields = ('resourceid',  'categoryid','classid',
                  'section','chapterid', 'resourcetype',
                  'originaltext','resourcetitle','resourcedescription',
                  'thumbnailurl','documenturl','imageurl',
                  'audiourl','videourl','createddate'
                  )

class WrittenworkinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Writtenworkinfo
        fields = ('writtenworkid',  'writtenworktitle','description',
                  'writtenimage','schoolid', 'classid','isassigned',
                  'createddate'
                  )

class StudentworkspaceinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Studentworkspaceinfo
        fields = ('workspaceid',  'workspacetitle','workspacetype',
                  'workspacetext','schoolid', 'classid','isassigned',
                  'posteddate'
                  )

class StudentnotesinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Notesinfo
        fields = ('notesid', 'notestitle','notes',
                  'isdeleted','createdby', 'createddate'
                  )

class StudentBulletinboardlistinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Bulletinboardinfo
        fields = ('messagetitle','message','posteddate','postedby')

class ClassroominfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Classroominfo
        fields = ('classroomid','assessmentid','resourceid','writtenworkid','studentid',
                  'rating','ratingcount','votescount','lastvotedby','lastvoteddate','postedby',
                  'posteddate')

class TopicsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Topicinfo
        fields = ('topicid',  'forumid','topicname','topicdetails',
                  'totalpost','createdby', 'createddate',
                  'lastpostedby','lastposteddate')

class PostinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Postinfo
        fields = ('postid', 'topicid','forumid',
                  'postdetails', 'postedby','posteddate','parentid')
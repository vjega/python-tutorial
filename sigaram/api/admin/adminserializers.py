from rest_framework import serializers
from portaladmin import models

class AdminInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Admininfo
        fields = ('adminid',  'firstname','lastname',
                  'username','emailid','imageurl')

class AdminFolderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AdminFolders
        fields = ('folder_id',  'folder_name','folder_description',
                  'added_date','folder_order')

class TeacherinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Teacherinfo
        fields = ('teacherid',  'username','password','classid',
                  'firstname','lastname', 'emailid','imageurl','schoolid')

class StudentinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Studentinfo
        fields = ('studentid',  'username','password',
                  'firstname','lastname', 'emailid',
                  'imageurl','schoolid','classid')

class TeacherResourcesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TeacherResources
        fields = ('resource_id',  'resourcetype','resourcetitle',
                  'resourcedescription','documenturl', 'imageurl',
                  'audiourl','videourl','resource_folder_id'
                  )

class  TeacherresourceinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Teacherresourceinfo
        fields = ('teacherresourceid',  'classid','section',
                  'chapterid','resourcetype', 'resourcecategory','originaltext',
                  'resourcetitle','resourcedescription','documenturl',
                  'imageurl','audiourl','videourl','schoolid','isapproved',
                  'createddate')


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
                  'writtenimage','schoolid', 'classid','isassigned')

class ChapterinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Chapterinfo
        fields = ('chapterid',  'classid','sectionid',
                  'chaptername')

class ClassroominfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Classroominfo
        fields = ('classroomid',  'assessmentid','resourceid',
                  'writtenworkid')
        depth = 2

class AdminschoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Schoolinfo
        fields = ('schoolid',  'schoolname','shortname',
                  'description','schoolimageurl','createdby','createddate')

class AdminclasslistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Classinfo
        fields = ('classid',  'classname','shortname',
                  'createdby','createddate')

class CalendarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Calendardetails
        fields = ('id',  'title','start','end')

class AdminrubricsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RubricsHeader
        fields = ('slno','title','description','teacher','status','ts')

class AssignresourceinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Assignresourceinfo
        fields = ('resourceid','studentid','assigntext','isanswered','assigneddate',
                    'isdelete','assignedby','issaved','originaltext','answertext','answerurl',
                    'isrecord','replyformat','isbillboard','isclassroom','answereddate',
                    'assignedby','assigneddate','isdelete','rubric_id','rubric_marks',
                    'rubric_n_mark','old_edit')

class WorkspaceinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Workspaceinfo
        fields = ('workspaceid','workspacetitle','workspacetype','posteddate','postedby',
                                                  'workspacetype','isapproved')

class MindmapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Mindmap
        fields = ('id','title','mapdata')

class StickynotesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.stickynotes
        fields = ('id','stickytext','color','name')
        
class StickyCommentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.stickycomments
        fields = ('id','stickyid','stickycomment','commentby')

class BulletinboardlistinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Bulletinboardinfo
        fields = ('messagetitle','message','posteddate','postedby')

class BillboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Billboardinfo
        fields = ('billboardid','assessmentid','resourceid','writtenworkid',
                  'studentid','votescount','lastvotedby','lastvoteddate','postedby',
                                                                        'posteddate')

class EditingtextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Editingtext
        fields = ('editingid', 'editid', 'spanid', 'previoustext', 'edittext', 'editedby', 
                  'editeddate', 'editedplace', 'typeofresource', 'usertype', 'isapproved', 
                                                                  'isrejected', 'oritxtrep');
class BulletinboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Classschoolmappinginfo
        fields = ('classid','schoolid')

class BulletinboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Classschoolmappinginfo
        fields = ('classid','schoolid')

class BulletinmappinginfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Bulletinmappinginfo
        fields = ('bulletinboardid','viewtype','schoolid','classid','adminid','teacherid',)

class TopicsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Topicinfo
        fields = ('topicid',  'forumid','topicname',
                  'totalpost','createdby', 'createddate',
                  'lastpostedby','lastposteddate')

class ThreadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Threaddetails
        fields = ('threadid', 'topicid','threadname',
                  'createdby', 'createddate')


class ExtraslistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Extraslist
        fields = ('extraid', 'resourceurl','title',
                'extratype','createddate')

class StickyinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Stickyinfo
        fields = ('id','title', 'createdby','isdeleted','createddate')

class LogininfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Logininfo
        fields = ('loginid','username', 'password','firstname','lastname','isdelete',
                   'lastlogin','usertype','isadmin')

class AudiouploadSerializer(serializers.HyperlinkedModelSerializer):
      class Meta:
        model = models.Admininfo
        fields = ('adminid',  'firstname','lastname',
                  'username','emailid','imageurl')

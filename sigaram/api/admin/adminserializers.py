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
        fields = ('teacherid',  'username','password',
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

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

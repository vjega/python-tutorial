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
                  'firstname','lastname', 'emailid','imageurl'
                  )

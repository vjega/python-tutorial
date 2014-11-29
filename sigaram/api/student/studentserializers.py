from rest_framework import serializers
from portaladmin import models

class StudentInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Admininfo
        fields = ('adminid',  'firstname','lastname',
                  'username','emailid','imageurl')


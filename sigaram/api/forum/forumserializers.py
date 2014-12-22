from rest_framework import serializers
from portalforum import models

class StudentinfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Studentinfo
        fields = ('studentid',  'username',
                  'firstname','lastname', 'emailid',
                  'imageurl','schoolid','classid')
        

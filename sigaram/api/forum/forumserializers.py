from rest_framework import serializers
from portaladmin import models

class ForuminfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Foruminfo
        fields = ('forumid',  'forumname','totaltopic',
                  'totalpost','createdby', 'createddate',
                  'lastpostedby','lastposteddate','isdelete')
        

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers

import viewsets

router = routers.DefaultRouter()
router.register(r'student',        	    viewsets.studentViewSet)
router.register(r'resourceinfo',   	    viewsets.ResourceinfoViewSet)
router.register(r'writtenworkinfo',     viewsets.WrittenworkinfoViewSet)
router.register(r'studentworkspaceinfo',viewsets.Studentworkspaceinfo)
router.register(r'studentnotesinfo', 	viewsets.StudentnotesinfoViewSet)
router.register(r'bulletinboardlist',   viewsets.Studentbulletinboardlist)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
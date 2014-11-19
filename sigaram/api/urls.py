from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers

import viewsets

router = routers.DefaultRouter()
router.register(r'admin',        viewsets.AdmininfoViewSet)
router.register(r'adminfolders', viewsets.AdminFoldersViewSet)
router.register(r'teacher',      viewsets.teacherViewSet)
router.register(r'student',      viewsets.studentViewSet)
router.register(r'teacherresources',      viewsets.TeacherResourcesViewSet)
router.register(r'teacherresourcesinfo',      viewsets.TeacherresourceinfoViewSet)
router.register(r'resourceinfo',          viewsets.ResourceinfoViewSet)
router.register(r'writtenworkinfo',       viewsets.WrittenworkinfoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
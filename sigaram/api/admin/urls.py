from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers

import viewsets

router = routers.DefaultRouter()
router.register(r'admin',        		  viewsets.AdmininfoViewSet)
router.register(r'adminfolders', 		  viewsets.AdminFoldersViewSet)
router.register(r'teacher',      		  viewsets.teacherViewSet)
router.register(r'student',      		  viewsets.studentViewSet)
router.register(r'teacherresources',      viewsets.TeacherResourcesViewSet)
router.register(r'teacherresourcesinfo',  viewsets.TeacherresourceinfoViewSet)
router.register(r'resourceinfo',          viewsets.ResourceinfoViewSet)
router.register(r'writtenworkinfo',       viewsets.WrittenworkinfoViewSet)
router.register(r'chapterinfo',           viewsets.ChapterinfoViewSet)
router.register(r'adminclassinfo',        viewsets.AdminclassinfoViewSet)
router.register(r'adminschool',        	  viewsets.AdminschoolViewSet)
router.register(r'classlist',             viewsets.AdminclasslistViewSet)
router.register(r'assignresourceinfo',    viewsets.AssignresourceinfoViewSet)
router.register(r'workspaceinfo',         viewsets.WorkspaceViewSet)
router.register(r'rubricsheader',         viewsets.AdminrubricsViewSet)
router.register(r'calendar',              viewsets.CalendarViewSet)
router.register(r'mindmap',                viewsets.MindmapViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
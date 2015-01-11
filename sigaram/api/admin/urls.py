from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers

import viewsets

router = routers.DefaultRouter()
router.register(r'admin',        		  	viewsets.AdmininfoViewSet)
router.register(r'adminfolders', 		  	viewsets.AdminFoldersViewSet)
router.register(r'teacher',      		  	viewsets.teacherViewSet)
router.register(r'student',      		  	viewsets.studentViewSet)
router.register(r'teacherresources',      	viewsets.TeacherResourcesViewSet)
router.register(r'teacherresourcesinfo',  	viewsets.TeacherresourceinfoViewSet)
router.register(r'resourceinfo',          	viewsets.ResourceinfoViewSet)
router.register(r'writtenworkinfo',       	viewsets.WrittenworkinfoViewSet)
router.register(r'chapterinfo',           	viewsets.ChapterinfoViewSet)
router.register(r'adminclassinfo',        	viewsets.AdminclassinfoViewSet)
router.register(r'adminschool',        	  	viewsets.AdminschoolViewSet)
router.register(r'classlist',             	viewsets.AdminclasslistViewSet)
router.register(r'assignresourceinfo',    	viewsets.AssignresourceinfoViewSet)
router.register(r'workspaceinfo',         	viewsets.WorkspaceViewSet)
router.register(r'rubricsheader',         	viewsets.AdminrubricsViewSet)
router.register(r'calendar',              	viewsets.CalendarViewSet)
router.register(r'mindmap',               	viewsets.MindmapViewSet)
router.register(r'stickynotes',           	viewsets.StickynotesResource)
router.register(r'studentassignresource', 	viewsets.StudentAssignResource)
router.register(r'teacherassignedresource', viewsets.TeacherStudentAssignResource)
router.register(r'assignedresourcestudents',viewsets.AssignedResourceStudents)
router.register(r'studentinfo',      	  	viewsets.StudentinfoViewSet)
router.register(r'stickycomments',          viewsets.StickyCommentsResource)
router.register(r'bulletinboardlist',       viewsets.Bulletinboardlist)
router.register(r'billboard',           	viewsets.BillboardViewSet)
router.register(r'editanswer',           	viewsets.EditAnswerViewSet)
router.register(r'bulletinboard',       	viewsets.Bulletinboard)
router.register(r'bulletinmappinginfo',     viewsets.Bulletinmappinginfo)
router.register(r'billboardresource',       viewsets.BillboardResourceViewSet)
router.register(r'topics',      			viewsets.TopicViewSet)
router.register(r'threads',      			viewsets.ThreadsViewSet)
router.register(r'rubrics',         		viewsets.RubricsViewSet)
router.register(r'extraslist',         		viewsets.ExtraslistViewSet)
router.register(r'stickyinfo',         		viewsets.StickyinfoViewSet)
router.register(r'auth_user',         		viewsets.AuthuserViewSet)
router.register(r'audioupload',         	viewsets.AudioinfoViewSet)
# router.register(r'adminresources',         	viewsets.AdminresourceViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers

import viewsets

router = routers.DefaultRouter()
router.register(r'admin',        		  	viewsets.AdmininfoViewSet)
router.register(r'adminfolders', 		  	viewsets.AdminFoldersViewSet)
router.register(r'teacher',      		  	viewsets.TeacherViewSet)
router.register(r'student',      		  	viewsets.studentViewSet)
router.register(r'teacherresources',      	viewsets.TeacherResourcesViewSet)
router.register(r'teacherresourcesinfo',  	viewsets.TeacherresourceinfoViewSet)
router.register(r'resourceinfo',          	viewsets.ResourceinfoViewSet)
router.register(r'studentresourceinfo',     viewsets.ResourceStudentinfoViewSet)
router.register(r'studentwrittenworkdetail',viewsets.StudentWrittenWorkDetailViewSet)
router.register(r'studentassessmentdetail', viewsets.StudentAssessmentDetailViewSet)
router.register(r'writtenworkinfo',       	viewsets.WrittenworkinfoViewSet)
router.register(r'chapterinfo',           	viewsets.ChapterinfoViewSet)
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
router.register(r'rubrics',         		viewsets.RubricsViewSet)
router.register(r'extraslist',         		viewsets.ExtraslistViewSet)
router.register(r'stickyinfo',         		viewsets.StickyinfoViewSet)
router.register(r'auth_user',         		viewsets.AuthuserViewSet)
router.register(r'audioupload',         	viewsets.AudioinfoViewSet)
router.register(r'adminresources',         	viewsets.AdminresourceViewSet)
router.register(r'classinfo',        		viewsets.ClassinfoViewSet)
router.register(r'studentwrittenwork', 		viewsets.StudentWrittenWork)
router.register(r'studentassignwrittenwork',viewsets.StudentAssignWrittenWork)
router.register(r'assignedwrittenworkstudents',viewsets.AssignedWrittenworkStudents)
router.register(r'editanswerresource',      viewsets.EditAnswerResourceViewSet)
router.register(r'editanswerwrittenwork',   viewsets.EditAnswerWrittenworkViewSet)
router.register(r'peerrubricsreview',   	viewsets.PeerRubricsReviewViewSet)
router.register(r'assignmindmapinfo',    	viewsets.AssignmindmapinfoViewSet)
router.register(r'teacherassignedmindmap',  viewsets.TeacherAssignedmindmapViewSet)
router.register(r'postinfo',    	        viewsets.PostinfoViewSet)
router.register(r'topicinfo',    	        viewsets.TopicInfoViewSet)
router.register(r'rubricimport',    	    viewsets.RubricImportViewSet)
router.register(r'assessmentinfo',    	    viewsets.AssessmentInfoViewSet)
router.register(r'billboardrating',    	    viewsets.BillboardRatingViewSet)
router.register(r'billboardcomment',    	viewsets.BillboardCommentViewSet)
router.register(r'richmindmap',    	        viewsets.RichmindmapViewSet)
router.register(r'studentwrittenworkinfo',  viewsets.studentwrittenworkViewSet)
router.register(r'myprofile',               viewsets.MyProfileViewSet)
router.register(r'assessmentqainfo',    	viewsets.AssessmentQAInfoViewSet)
router.register(r'studentassignassessment', viewsets.StudentAssignAssessment)
router.register(r'activityloginfo',    		viewsets.ActivitylogInfoViewSet)
router.register(r'activityassignment',    	viewsets.ActivityassignmentInfoViewSet)
router.register(r'studentassignedresource', viewsets.StudentassignedresourceInfoViewSet)
router.register(r'assignmentanswerrating',  viewsets.AssignmentRatingViewSet)
router.register(r'activityassessment', 		viewsets.ActivityassessmentInfoViewSet)
router.register(r'studentassessmentinfo', 	viewsets.studentAssessmentInfoViewSet)
router.register(r'assessmentstatistics', 	viewsets.AssessmentstatisticsInfo)
router.register(r'statisticsstudent', 		viewsets.StatisticsstudentInfo)
router.register(r'viewassignassessment', 	viewsets.ViewassignassessmentInfo)
router.register(r'studentopenendedInfoViewSet', viewsets.studentopenendedInfoViewSet)
router.register(r'teacherassessmentinfo', 	viewsets.teacherAssessmentInfoViewSet)
router.register(r'activitywrittenwork', 	viewsets.activitywrittenworkInfoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
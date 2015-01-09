from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers

import viewsets

router = routers.DefaultRouter()
router.register(r'foruminfo',      viewsets.ForuminfoViewSet)
router.register(r'topicinfo',      viewsets.TopicinfoViewSet)
router.register(r'postreplyinfo',  viewsets.PostreplyinfoViewSet)
router.register(r'postinfo',       viewsets.PostinfoViewSet)
router.register(r'activitylog',    viewsets.ActivitylogViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
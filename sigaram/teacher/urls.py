#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from teacher import views

urlpatterns = patterns('student.views',
    url(r'^home$',                  'home',         name='home'),
    
)

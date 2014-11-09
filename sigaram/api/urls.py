#Portal Routing
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from api.views import admin

urlpatterns = patterns('',
    url(r'^admin/addfolder$',      admin.addfolder,     name='addfolder'),
)

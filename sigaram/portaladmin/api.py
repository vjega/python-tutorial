from tastypie.resources import ModelResource
from portaladmin.models import AdminFolders


class AdminFoldersResource(ModelResource):
    class Meta:
        queryset = AdminFolders.objects.all()
        resource_name = 'admin_folders'
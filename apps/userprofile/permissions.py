from rest_framework import permissions


class HasApplicationAdminAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.has_access(request.user, obj.get_admin_uri())
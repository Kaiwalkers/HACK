from rest_framework.permissions import BasePermission


class MoviePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff and request.user.is_superuser



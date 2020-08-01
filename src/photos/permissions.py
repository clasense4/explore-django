from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Admin can have access
        if request.user.is_staff:
            return True

        # Write permissions are only allowed to the user of the photos.
        return obj.user == request.user
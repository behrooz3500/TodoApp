from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ A custom permission to allow only a task owner make changes to it. """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.user == request.user

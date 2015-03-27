from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #obj is account
        if request.user:
            return obj == request.user
        return False
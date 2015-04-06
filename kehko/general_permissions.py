from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #obj is account
        if request.user:
            return obj == request.user
        return False

class IsCompanyAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj.account_owner == request.user
        return False
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

class HasRightsToUploadImage(permissions.BasePermission):
    """
    Object is either Company instance or None
    If Company, check that the user is allowed to post for the company
    Else check that the user is authenticated
    """
    def has_object_permission(self, request, view, obj):
        if obj:
            return obj.account_owner == request.user
        else:
            if request.user:
                return True
            else:
                return False
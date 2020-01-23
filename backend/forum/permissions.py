from rest_framework.permissions import BasePermission


class IsAuthenticatedOnCreateUpdate(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT']:
            return bool(request.user and request.user.is_authenticated)
        else:
            return True

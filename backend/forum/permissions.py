from rest_framework.permissions import BasePermission


class IsAdminOnCreateUpdateDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'DELETE']:
            return bool(request.user and request.user.is_staff)
        else:
            return True


class IsAuthenticatedOnCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return bool(request.user and request.user.is_authenticated)
        else:
            return True


class IsAuthenticatedOnUpdate(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT']:
            return bool(request.user and request.user.is_authenticated)
        else:
            return True


class IsAuthenticatedOnDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['DELETE']:
            return bool(request.user and request.user.is_authenticated)
        else:
            return True


class IsAuthenticatedOnCreateUpdateDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'DELETE']:
            return bool(request.user and request.user.is_authenticated)
        else:
            return True

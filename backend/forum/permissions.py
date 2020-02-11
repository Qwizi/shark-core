from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOnCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return bool(request.user and request.user.is_staff)
        else:
            return True


class IsAdminOnUpdate(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['UPDATE']:
            return bool(request.user and request.user.is_staff)
        else:
            return True


class IsAdminOnDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['DELETE']:
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


class IsAuthorOnNotSafeMethods(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return bool(request.user == obj.author)
        else:
            return True

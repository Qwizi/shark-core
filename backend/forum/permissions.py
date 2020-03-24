from rest_framework.permissions import BasePermission, SAFE_METHODS


class ThreadPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        else:
            return False


class IsAuthorOnReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class PostPermission(ThreadPermission):
    pass

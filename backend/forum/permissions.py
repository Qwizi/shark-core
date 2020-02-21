from rest_framework.permissions import BasePermission, SAFE_METHODS


class ThreadPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        else:
            return False


class PostPermission(ThreadPermission):
    pass

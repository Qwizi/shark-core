from rest_framework import permissions


class SteamBotQueuePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        else:
            return False

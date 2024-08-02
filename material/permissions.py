from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(group_id=2).exists():
            return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user




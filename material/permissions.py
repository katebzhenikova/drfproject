from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Модераторы').exists():
            return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsUserOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем аккаунта"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user

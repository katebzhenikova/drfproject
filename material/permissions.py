from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Модераторы').exists():
            return True


class IsOwner(BasePermission):
    def has_permission(self, request, view):

        return request.user == view.get_object().owner

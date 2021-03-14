from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsCarPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'C')


class IsMechanicPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'M')

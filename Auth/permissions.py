from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsReadOnlyAllRolePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.method in SAFE_METHODS)


class IsCarPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'C')


class IsCarReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'C'
                    and request.method in SAFE_METHODS)


class IsMechanicPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'M')


class IsMechanicReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'M'
                    and request.method in SAFE_METHODS)


class IsAdminPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'A')


class IsAdminReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'A'
                    and request.method in SAFE_METHODS)


class IsDriverPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'D')


class IsDriverReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'D'
                    and request.method in SAFE_METHODS)
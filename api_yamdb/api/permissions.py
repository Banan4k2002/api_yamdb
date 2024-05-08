from rest_framework import permissions

from .constants import REQUESTED_ROLE_ADMIN


class IsAnonReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AuthenticatedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class AuthorPermission(AuthenticatedPermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ModeratorPermission(AuthenticatedPermission):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and request.user.is_moderator
        )

    def has_object_permission(self, request, view, obj):
        return (
            super().has_object_permission(request, view, obj)
            or request.user.is_moderator
        )


class OnlyAdminPostPermissons(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        else:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.role == REQUESTED_ROLE_ADMIN
                or request.user.is_superuser
            )


class AdminPermission(AuthenticatedPermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return (
            super().has_object_permission(request, view, obj)
            or request.user.is_admin
        )


class SuperUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

from rest_framework import permissions


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

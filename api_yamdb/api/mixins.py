from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.permissions import (
    AdminPermission,
    AuthorPermission,
    DisablePUTMethod,
    IsAnonReadOnlyPermission,
    ModeratorPermission,
    OnlyAdminPostPermissons,
)


class CreateDestroyListViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    """Миксин для жанров и категорий"""

    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (OnlyAdminPostPermissons,)


class PublicationPermissionViewSet(ModelViewSet):
    permission_classes = (AuthorPermission, DisablePUTMethod)

    def get_permissions(self):
        if self.request.user.is_anonymous:
            return (IsAnonReadOnlyPermission(), DisablePUTMethod())
        elif self.request.user.is_moderator:
            return (ModeratorPermission(), DisablePUTMethod())
        elif self.request.user.is_admin:
            return (AdminPermission(), DisablePUTMethod())
        return super().get_permissions()

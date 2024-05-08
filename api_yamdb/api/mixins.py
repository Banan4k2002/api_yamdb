from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet

from .permissions import OnlyAdminPostPermissons


class CreateDestroyListViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    """Миксин для жанров и категорий"""

    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (OnlyAdminPostPermissons,)

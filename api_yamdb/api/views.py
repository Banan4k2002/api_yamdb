from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from reviews.models import Category, Genre, Title

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleCreteUpdateSerializer)


class DictViewMixin(CreateModelMixin,
                    DestroyModelMixin,
                    ListModelMixin,
                    GenericViewSet):
    """Михин для жанров и категорий"""
    pass


class CategoryViewset(DictViewMixin):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(DictViewMixin):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.all()
    filter_backends = (SearchFilter,)
    # serializer_class = TitleSerializer
    search_fields = ('name', 'year', 'description',
                     'genre__slug', 'category__slug')

    def get_serializer_class(self):
        print(self.action)
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreteUpdateSerializer
        return TitleSerializer

    def handle_create_update(self, serializer):
        """Обработка сохранения данных с переключением сериализатора."""
        if serializer.is_valid():

            obj = serializer.save()
            serializer = TitleSerializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        return self.handle_create_update(serializer)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        return self.handle_create_update(serializer)

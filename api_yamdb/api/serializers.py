import datetime as dt

from django.shortcuts import get_object_or_404

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SlugRelatedField

from reviews.models import Category, Genre, GenreTitle, Title


class CategorySerializer(ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(ModelSerializer):
    """Сериализатор произведений."""
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', 'rating')


class TitleCreteUpdateSerializer(ModelSerializer):
    genre = SlugRelatedField(many=True,
                             slug_field='slug',
                             queryset=Genre.objects.all())
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', 'rating')

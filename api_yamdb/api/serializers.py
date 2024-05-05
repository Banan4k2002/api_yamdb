import datetime as dt

from django.shortcuts import get_object_or_404

from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.serializers import SlugRelatedField

from reviews.constants import NAME_MAX_LENGTH, SLUG_MAX_LENGTH
from reviews.models import Category, Genre, GenreTitle, Title


class CategorySerializer(ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category

    def validate_name(self, value):
        if len(value) > NAME_MAX_LENGTH:
            raise ValidationError(f'Длина имени больше {NAME_MAX_LENGTH}.')
        return value

    def validate_slug(self, value):
        if len(value) > SLUG_MAX_LENGTH:
            raise ValidationError(f'Длина слага больше {SLUG_MAX_LENGTH}.')
        return value


class GenreSerializer(ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre

    def validate_name(self, value):
        if len(value) > NAME_MAX_LENGTH:
            raise ValidationError(f'Длина имени больше {NAME_MAX_LENGTH}.')
        return value

    def validate_slug(self, value):
        if len(value) > SLUG_MAX_LENGTH:
            raise ValidationError(f'Длина слага больше {SLUG_MAX_LENGTH}.')
        return value


class TitleSerializer(ModelSerializer):
    """Сериализатор произведений."""
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', 'rating')

    def validate_year(self, value):
        if value > dt.date.today().year:
            return ValidationError('Произведение еще не создано.')
        return value


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

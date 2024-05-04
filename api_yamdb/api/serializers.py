
import datetime as dt

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField, ValidationError, StringRelatedField

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
    genres = GenreSerializer(many=True, required=False, source='genre')
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genres', 'category')
        read_only_fields = ('')

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise ValidationError('Год создания произведения больше текщего.')

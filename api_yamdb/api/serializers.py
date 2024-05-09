import re

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import ValidationError

from reviews.constants import NAME_MAX_LENGTH, SLUG_MAX_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class BaseNameSlugSerializer(serializers.ModelSerializer):
    """Базовый ссериализатор дл полей name и slug."""

    def validate_name(self, value):
        if len(value) >= NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Длина поля name больше {NAME_MAX_LENGTH}.'
            )
        return value

    def validate_slug(self, value):
        if len(value) >= SLUG_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Длина поля slug больше {SLUG_MAX_LENGTH}.'
            )
        if not re.match(r'^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'Некорректное значение поля slug'
            )
        return value


class CategorySerializer(BaseNameSlugSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(BaseNameSlugSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )

        extra_kwargs = {
            'genre': {'requered': False},
            'year': {'required': False},
            'category': {'required': False},
        }


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=False,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=False
    )
    year = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )
        

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Использовать имя me запрещено')
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Пользователь с такой фамилией уже существует'
            )
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$', max_length=150, required=True
    )
    confirmation_code = serializers.CharField(max_length=150, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('id', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            data['title'] = self.context.get('view').get_title()
            data['author'] = request.user
            if Review.objects.filter(
                author=data['author'],
                title=data['title'],
            ).exists():
                raise ValidationError(
                    'На произведение можно оставить только один отзыв'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('id', 'pub_date')

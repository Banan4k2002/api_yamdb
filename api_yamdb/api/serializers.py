import datetime as dt
import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.constants import NAME_MAX_LENGTH, SLUG_MAX_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category

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


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre

    def validate_name(self, value):
        if len(value) >= NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Длина имени больше {NAME_MAX_LENGTH}.'
            )
        return value

    def validate_slug(self, value):
        if len(value) >= SLUG_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Длина слага больше {SLUG_MAX_LENGTH}.'
            )
        return value


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
            'category': {'required': False}
        }

    def validate_year(self, value):
        if value > dt.date.today().year:
            return serializers.ValidationError('Произведение еще не создано.')
        return value


class TitleCreteUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
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
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с такой фамилией уже существует'
            )
        if User.objects.filter(email=data.get('email')):
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

    def validate_username(self, username):
        if username in 'me':
            raise serializers.ValidationError('Имя me запрещено')
        return username


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review
        read_only_fields = ('id', 'pub_date')
        extra_kwargs = {'title': {'required': False}}


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('id', 'pub_date')

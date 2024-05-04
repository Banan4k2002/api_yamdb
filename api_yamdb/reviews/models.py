import datetime as dt

from django.db import models
from django.db.models import CheckConstraint

from .constants import NAME_MAX_LENGTH, SLUG_MAX_LENGTH


class Category(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True, max_length=SLUG_MAX_LENGTH)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True, max_length=SLUG_MAX_LENGTH)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    year = models.IntegerField('Год')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='titles', null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

        constraints = [
            CheckConstraint(
                check=models.Q(year__lte=dt.date.today().year),
                name='check_title_year'
            )
        ]

    @property
    def rating(self):
        data = self.reviews.aggregate(models.Avg('score'))
        return round(data.get('score__avg'))

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

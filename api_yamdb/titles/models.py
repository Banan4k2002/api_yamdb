from django.db import models

from .constants import NAME_MAX_LENGTH


class Category(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField()


class Title(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    year = models.IntegerField('Год')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                 related_name='titles')


class GenreTitle(models.Model):
    Title = models.ForeignKey(Title, on_delete=models.DO_NOTHING,
                              related_name='genres')
    Genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)

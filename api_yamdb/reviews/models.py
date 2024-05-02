from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .constants import NAME_MAX_LENGTH


class Category(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    year = models.IntegerField('Год')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='genres'
    )
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    text = models.TextField('Текст отзыва')
    author = models.IntegerField('Автор')  # models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10),
        ),
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'), name='unique_author_title'
            ),
            models.CheckConstraint(
                check=models.Q(score__range=(1, 10)), name='check_score'
            ),
        )

    def __str__(self):
        return f'{self.title.name} - {self.score}'

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from reviews.constants import NAME_MAX_LENGTH, SLUG_MAX_LENGTH

User = get_user_model()


def title_year_validation(value):
    """Функция валидации года."""
    if value > timezone.now().year:
        raise ValidationError('Год не может быть больше текущего.')
    return value


class BaseNameSlugModel(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True, max_length=SLUG_MAX_LENGTH)

    class Meta:
        abstract = True


class Category(BaseNameSlugModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(BaseNameSlugModel):

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
    genre = models.ManyToManyField(Genre)
    description = models.TextField('Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def rating(self):
        data = self.reviews.aggregate(models.Avg('score'))
        return data.get('score__avg')

    def __str__(self):
        return self.name


class BasePublicationModel(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)s'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True


class Review(BasePublicationModel):
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1, 'Оценка не может быть меньше чем 1'),
            MaxValueValidator(10, 'Оценка не может быть больше чем 10'),
        ),
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
        )

    def __str__(self):
        return f'{self.title.name} - {self.score}'


class Comment(BasePublicationModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

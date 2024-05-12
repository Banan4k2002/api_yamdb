from django.core.exceptions import ValidationError
from django.utils import timezone


def title_year_validation(value):
    """Функция валидации года."""
    if value > timezone.now().year:
        raise ValidationError('Год не может быть больше текущего.')
    return value

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class UserRole:
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    CHOICES = (
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор"),
    )


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит некорректный символ'
        )]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        "Роль пользователя",
        max_length=20,
        default=UserRole.USER,
        choices=UserRole.CHOICES,
    )
    confirmation_code = models.CharField(
        "Код авторизации", max_length=15, blank=True, null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"],
                name="unique_user"
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.is_superuser
            or self.role == UserRole.ADMIN
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

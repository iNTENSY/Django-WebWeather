from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_PERMISSIONS: tuple[tuple[str]] = (
        ('Default', 'Default'),
        ('Premium', 'Premium'),
    )
    user_status = models.CharField(
        max_length=10,
        verbose_name='Статус',
        choices=USER_PERMISSIONS,
        default='Default',
        blank=True
    )

    class Meta:
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'
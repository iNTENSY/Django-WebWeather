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


class PaymentModel(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='User',
        on_delete=models.SET_NULL,
        null=True
    )
    uuid = models.UUIDField(
        verbose_name='Уникальный код'
    )
    is_accepted = models.BooleanField(
        verbose_name='Статус платежа',
        default=False,
        blank=True
    )

    class Meta:
        verbose_name: str = 'Платёж'
        verbose_name_plural: str = 'Платёжи'

    def __str__(self) -> str:
        return f'{self.user} [{self.uuid}]'
import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.http import Http404
from django.shortcuts import get_object_or_404


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


class Subscription(models.Model):
    client = models.ForeignKey(
        verbose_name='Покупатель',
        to='User',
        on_delete=models.PROTECT,
        related_name='subscription'
    )
    order = models.ForeignKey(
        verbose_name='Платёж',
        to='PaymentModel',
        on_delete=models.SET_NULL,
        null=True,
        related_name='subscription'
    )
    start_date = models.DateField(
        verbose_name='Дата старта подписки',
        blank=True
    )
    end_date = models.DateField(
        verbose_name='Дата окончания подписки',
        blank=True
    )

    class Meta:
        verbose_name: str = 'Подписка'
        verbose_name_plural: str = 'Подписки'

    def __str__(self) -> str:
        return f'Подписка {self.id}'


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
    date = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name: str = 'Платёж'
        verbose_name_plural: str = 'Платёжи'

    def __str__(self) -> str:
        return f'{self.uuid}'


@receiver(pre_save, sender=Subscription)
def subscription_handler(instance: Subscription, **kwargs):
    try:
        sub = get_object_or_404(
            Subscription.objects.order_by('end_date'),
            client=instance.client
        )
    except Http404:
        return

    date_checker = sub.end_date if sub.end_date >= dt.date.today() else dt.date.today()

    instance.start_date = date_checker
    instance.end_date = date_checker + dt.timedelta(days=30)

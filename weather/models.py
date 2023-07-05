from django.db import models
from django.shortcuts import get_object_or_404


class Cities(models.Model):
    """
    Модель базы данных:
    name - название города,
    total_searches - количество поиска данного города,
    last_search - дата последнего поиска данного города.
    """
    name = models.CharField(
        verbose_name='Название города',
        max_length=40
    )
    total_searches = models.IntegerField(
        verbose_name='Количество поиска',
        default=0
    )
    last_search = models.DateTimeField(
        verbose_name='Дата последнего поиска',
        auto_now=True
    )

    class Meta:
        verbose_name: str = 'Город'
        verbose_name_plural: str = 'Города'

    def __str__(self) -> str:
        return self.name

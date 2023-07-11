from django.utils import timezone

from weather.models import Cities

from celery import shared_task


@shared_task
def counter(city: str) -> str:
    """
    Данная функция добавляет единицу в total_searches,
    если переданный ей город модели Cities существует, или создает
    его сама. Независимо от выбора действий, функция
    устанавливает новую дату в графу "last_search".
    """
    try:
        record = Cities.objects.get(name=city)
    except Cities.DoesNotExist:
        record = None
    date: timezone = timezone.now()
    if record is not None:
        record.total_searches += 1
        record.last_search = timezone.now()
        record.save()
        return 'New settings saved'
    else:
        Cities.objects.create(
            name=city.capitalize(),
            total_searches=1,
            last_search=date
        )
        return 'New object created!'
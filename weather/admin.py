from django.contrib import admin

from .models import Cities


@admin.register(Cities)
class CitiesAdminPanel(admin.ModelAdmin):
    """Панель администратора с возможностью сортировки и поиска городов."""
    list_display: tuple[str] = ('name', 'total_searches', 'last_search')
    search_fields: tuple[str] = ('name',)
    ordering: tuple[str] = ('name', 'total_searches')
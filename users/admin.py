from django.contrib import admin

from users.models import User, PaymentModel, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display: tuple[str] = ('username', 'user_status')


@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display: tuple[str] = ('uuid', 'user', 'is_accepted', 'date')
    readonly_fields: tuple[str] = ('uuid', 'user', 'is_accepted', 'date')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display: tuple[str] = ('client', 'order', 'start_date', 'end_date')
    readonly_fields: tuple[str] = ('client', 'order', 'start_date', 'end_date')

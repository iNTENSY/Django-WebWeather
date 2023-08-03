from django.contrib import admin

from users.models import User, PaymentModel


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_status')


@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'is_accepted')
    readonly_fields = ('uuid', 'user', 'is_accepted')


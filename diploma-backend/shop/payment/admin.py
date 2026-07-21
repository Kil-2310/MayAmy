from django.contrib import admin

from .models import CreditCard


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    """Админка для кредиток клиентов"""

    list_display = ('number', 'month', 'year', 'code', 'profile', )
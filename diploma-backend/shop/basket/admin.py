from django.contrib import admin

from .models import Basket


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """Модель админки для корзины клиента"""

    fields = ('id', 'product', 'user', 'count', )

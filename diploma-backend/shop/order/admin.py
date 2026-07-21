from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    """Инлайн модель категории в заказе"""
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('totalCost', 'city', 'address', 'status', 'deliveryType', )

    inlines = [OrderItemInline]

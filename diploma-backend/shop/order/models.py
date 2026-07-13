from django.db import models

from product.models import Product
from user_profile.models import Profile


class Order(models.Model):
    """Модель заказа"""

    createdAt = models.DateTimeField(auto_now_add=True)
    paymentType = models.CharField(max_length=50)
    totalCost = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="pending")
    deliveryType = models.CharField(max_length=50)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='order_profile')


class OrderItem(models.Model):
    """Позиции в казазе"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_item')

    count = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

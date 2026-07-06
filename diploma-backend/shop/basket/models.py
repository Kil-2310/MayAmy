from django.contrib.auth.models import User
from django.db import models

from catalog.models import Product


class Basket(models.Model):
    """Корзина клиента"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

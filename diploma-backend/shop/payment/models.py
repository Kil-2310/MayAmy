from django.db import models

from user_profile.models import Profile


class CreditCard(models.Model):
    """Кредитная карта пользователя"""

    number = models.CharField(max_length=11, unique=True)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    code = models.CharField(max_length=3)

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='credit_card')

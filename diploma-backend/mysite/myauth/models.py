from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Профиль пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='profile_pics')
    phone =models.CharField(max_length=20)


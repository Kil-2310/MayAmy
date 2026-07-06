from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Профиль пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullName = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)


class ProfileAvatar(models.Model):
    """Аватар пользователя"""

    alt = models.CharField(max_length=255)
    preview = models.ImageField()
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='avatar')

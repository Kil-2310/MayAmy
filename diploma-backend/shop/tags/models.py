from django.db import models

class Tag(models.Model):
    """Тэг"""

    name = models.CharField(max_length=255, unique=True)
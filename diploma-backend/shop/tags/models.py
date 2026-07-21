from django.db import models


class Tag(models.Model):
    """Тэг"""

    class Meta:
        ordering = ('pk', )

    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

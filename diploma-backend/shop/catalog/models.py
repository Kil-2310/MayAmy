from django.db import models


class Category(models.Model):
    """Котегория продуктов"""

    title = models.CharField(max_length=100, verbose_name='Название категории')
    image = models.ImageField(upload_to='categories/', verbose_name='Иконка')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
    )

    def __str__(self):
        return f"{self.title}"

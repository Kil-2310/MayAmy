from django.db import models


class CatalogPreview(models.Model):
    """Превью"""

    preview = models.ImageField(upload_to='catalog_preview/')
    alt = models.CharField(max_length=255)


class Category(models.Model):
    """Главная категория продукта"""

    title = models.CharField(max_length=255, unique=True)
    image = models.OneToOneField(CatalogPreview, on_delete=models.CASCADE, null=True)


class Subcategory(models.Model):
    """Подкатегория продукта"""

    title = models.CharField(max_length=255)

    image = models.OneToOneField(CatalogPreview, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

from django.db import models


class CategoryPreview(models.Model):
    """Превью для главной категории"""

    preview = models.ImageField(upload_to='category_preview/')
    alt = models.CharField(max_length=255)

    def __str__(self):
        return self.alt


class SubcategoryPreview(models.Model):
    """Превью для подкатегорий"""

    preview = models.ImageField(upload_to='subcategory_preview/')
    alt = models.CharField(max_length=255)

    def __str__(self):
        return self.alt


class Category(models.Model):
    """Главная категория продукта"""

    title = models.CharField(max_length=255, unique=True)
    image = models.OneToOneField(CategoryPreview, on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return f"Category: {self.title}"


class Subcategory(models.Model):
    """Подкатегория продукта"""

    title = models.CharField(max_length=255, unique=True)

    image = models.OneToOneField(SubcategoryPreview, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"Subcategory: {self.title}"

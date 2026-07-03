from django.db import models

from django.shortcuts import get_object_or_404

# TODO перенести в отдельное приложеине
class Tag(models.Model):
    """Тэг"""

    name = models.CharField(max_length=255, unique=True)

class Image(models.Model):
    """Превью"""

    preview = models.ImageField(upload_to='products/')
    alt = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    """Главная категория продукта"""

    title = models.CharField(max_length=255, unique=True)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, null=True)

class Subcategory(models.Model):
    """Подкатегория продукта"""

    title = models.CharField(max_length=255)

    image = models.OneToOneField(Image, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')


# TODO перенести в отдельное приложеине и создать моель для отзываоа
class Product(models.Model):
    """Товар"""

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    count = models.PositiveIntegerField(default=0)
    freeDelivery = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    reviews = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products')


    @classmethod
    def get_by_id(cls, id: int) -> 'Product':
        """Получение продукта по id или 404"""

        return get_object_or_404(cls, id=id)

class Sales(models.Model):
    """Проданные продукты"""

    salePrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dateFrom = models.DateField()
    dateTo = models.DateField()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')

class Banner(models.Model):
    """Банеры"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='banners')

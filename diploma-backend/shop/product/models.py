from django.db import models

from catalog.models import Category
from tags.models import Tag
from django.contrib.auth.models import User


class ProductPreview(models.Model):
    """Картинки для продуктов"""

    preview = models.ImageField(upload_to='products_preview/')
    alt = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.alt


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
    isLimited = models.BooleanField(default=False)

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    images = models.ManyToManyField(ProductPreview, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products')


    def __str__(self) -> str:
        return self.title


class ProductReviews(models.Model):
    """Отзывы клиентов"""

    text = models.TextField()
    rate = models.SmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')

    def __str__(self) -> str:
        return self.user.username


class Specifications(models.Model):
    """Спецификация товара"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Sales(models.Model):
    """Проданные продукты"""

    salePrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dateFrom = models.DateField()
    dateTo = models.DateField()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')

    def __str__(self) -> str:
        return self.product.title


class Banner(models.Model):
    """Банеры"""

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='banner')

    def __str__(self) -> str:
        return self.product.title

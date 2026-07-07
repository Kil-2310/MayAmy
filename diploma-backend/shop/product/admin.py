from django.contrib import admin

from .models import (
    Product,
    ProductReviews,
    Banner,
    Sales,
    Specifications
)

# TODO После окончания разработки каталога подключить Sales и Banner

class ProductReviewsInline(admin.StackedInline):
    """Инлайн модель отзывов"""

    model = ProductReviews


class SpecificationsInline(admin.StackedInline):
    """Инлайн модель спецификации"""

    model = Specifications


class TagInline(admin.StackedInline):
    """Инлайн модель тэга"""

    model = Product.tags.through


class CategoryInline(admin.StackedInline):
    """Инлайн модель подкатегории"""

    model = Product.category.through


class ProductPreviewInline(admin.StackedInline):
    """Инлайн модель превью для товаров"""

    model = Product.images.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Модель админки для продукта"""

    list_display = (
        'id',
        'title',
        'description',
        'price',
        'count',
        'freeDelivery',
        'date',
        'reviews',
        'rating',
        'isLimited',

    )

    inlines = [
        SpecificationsInline,
        ProductReviewsInline,
        TagInline,
        CategoryInline,
        ProductPreviewInline,
    ]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """Модель админки для баннеров"""

    list_display = (
        'product__title',
    )


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    """Модель админки для проданных товаров"""

    list_display = (
        'product__title',
    )

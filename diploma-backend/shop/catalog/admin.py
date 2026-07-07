from django.contrib import admin

from .models import Category, Subcategory, CatalogPreview


class CategoryInline(admin.StackedInline):
    """Инлайн модель для главной категории"""

    model = Category


class SubcategoryInline(admin.StackedInline):
    """Инлайн модель для подкатегории"""

    model = Subcategory


@admin.register(CatalogPreview)
class CatalogPreviewAdmin(admin.ModelAdmin):
    """Админка для превью с категориями и подкатегориями"""

    list_display = ('id', 'alt', 'preview')

    inlines = [CategoryInline, SubcategoryInline]
from django.contrib import admin

from .models import Category, Subcategory, SubcategoryPreview, CategoryPreview


class CategoryInline(admin.StackedInline):
    """Инлайн модель для главной категории"""

    model = Category


class SubcategoryInline(admin.StackedInline):
    """Инлайн модель для подкатегории"""

    model = Subcategory


@admin.register(CategoryPreview)
class CatalogPreviewAdmin(admin.ModelAdmin):
    """Админка для превью с категориями"""

    list_display = ('id', 'alt', 'preview')

    inlines = [CategoryInline]


@admin.register(SubcategoryPreview)
class CatalogPreviewAdmin(admin.ModelAdmin):
    """Админка для превью с подкатегориями"""

    list_display = ('id', 'alt', 'preview')

    inlines = [SubcategoryInline]

from django.contrib import admin

from .models import Category


class SubcategoryInline(admin.StackedInline):
    """Инлайн модель подкатегорий"""

    model = Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Модель админки для категории"""

    list_display = ('id', 'title', 'image', 'parent', )
    inlines = [
        SubcategoryInline,
    ]

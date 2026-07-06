from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Модель админки для тэга"""

    list_display = ('pk', 'name',)

from django.contrib import admin

from .models import Profile, ProfileAvatar


class ProfileAvatarInline(admin.StackedInline):
    """Связная модель аватара для профиля"""

    model = ProfileAvatar


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Модкль админки для профиля"""

    list_display = ('pk', 'user', 'fullName', 'phone', 'user__email', )
    list_select_related = ('user',)
    inlines = [ProfileAvatarInline]

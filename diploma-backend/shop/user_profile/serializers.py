from typing import Union

from rest_framework import serializers

from .models import Profile, ProfileAvatar


class ProfileAvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватвра в профиле"""

    src = serializers.SerializerMethodField()

    class Meta:
        model = ProfileAvatar
        fields = ('alt', 'src')

    def get_src(self, obj: ProfileAvatar) -> Union[str, None]:
        """Проверка пути до превью"""

        if obj and obj.preview:
            return obj.preview.url
        return None

class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля"""

    avatar = ProfileAvatarSerializer()
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Profile
        fields = ('fullName', 'email', 'phone', 'avatar')


class UpdateProfileSerializer(serializers.Serializer):
    """Сериализатор для обновления профиля пользователя"""

    email = serializers.EmailField()
    phone = serializers.CharField()
    fullName = serializers.CharField()


class UpdatePasswordSerializer(serializers.Serializer):
    """Сериализатор для обновления пароля"""

    currentPassword = serializers.CharField()
    newPassword = serializers.CharField()

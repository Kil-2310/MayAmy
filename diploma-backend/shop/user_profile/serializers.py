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


class UpdateAvatarSerializer(serializers.Serializer):
    """Сериалайзер для аватара"""

    avatar = serializers.ImageField(required=True, allow_empty_file=False)

    def validate_avatar(self, value):
        """Дополнительная валидация изображения"""

        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                f'Image size must not exceed {max_size // (1024 * 1024)}MB'
            )

        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                f'Unsupported file type. Allowed: {", ".join(allowed_types)}'
            )

        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        if not any(value.name.lower().endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError(
                f'Unsupported file extension. Allowed: {", ".join(allowed_extensions)}'
            )

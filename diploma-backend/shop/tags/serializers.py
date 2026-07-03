from rest_framework import serializers

from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
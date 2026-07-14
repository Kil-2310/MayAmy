from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов"""

    class Meta:
        model = Tag
        fields = ('id', 'name')

class PostTagsSerializer(serializers.Serializer):
    """Отправка тэгов"""

    id = serializers.IntegerField()
    name = serializers.CharField()
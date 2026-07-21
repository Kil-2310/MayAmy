from typing import Dict

from rest_framework import serializers
from .models import Category


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий"""

    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'image',)


    def get_image(self, obj: Category) -> Dict[str, str]:

        return {
            'src': obj.image.url if obj.image else None,
            'alt': obj.title
        }


class MainCategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для главных категорий"""

    subcategories = SubcategorySerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories',)

    def get_image(self, obj: Category) -> Dict[str, str]:

        return {
            'src': obj.image.url if obj.image else None,
            'alt': obj.title
        }

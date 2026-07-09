from typing import Union

from rest_framework import serializers

from .models import (
    Category,
    Subcategory,
    CategoryPreview,
    SubcategoryPreview,
)


class CatalogPreviewSerializer(serializers.ModelSerializer):
    """Сериализатор превью"""
    src = serializers.SerializerMethodField()

    class Meta:
        model = CategoryPreview
        fields = ('src', 'alt')

    def get_src(self, obj: CategoryPreview) -> Union[None, str]:
        if obj.preview:
            return obj.preview.url
        return None


class SubcategoryPreviewSerializer(serializers.ModelSerializer):
    """Сериализатор превью"""
    src = serializers.SerializerMethodField()

    class Meta:
        model = SubcategoryPreview
        fields = ('src', 'alt')

    def get_src(self, obj):
        if obj.preview:
            return obj.preview.url
        return None


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории"""

    image = SubcategoryPreviewSerializer()

    class Meta:
        model = Subcategory
        fields = ('id', 'title', 'image')


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категории"""

    image = CatalogPreviewSerializer()
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')

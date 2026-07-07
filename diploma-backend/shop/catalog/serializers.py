from rest_framework import serializers

from .models import (
    Category,
    Subcategory,
    CatalogPreview,
)
from product.models import Sales


class CatalogPreviewSerializer(serializers.ModelSerializer):
    """Сериализатор превью"""

    src = serializers.SerializerMethodField()

    class Meta:
        model = CatalogPreview
        fields = ('src', 'alt')

    def get_src(self, obj):
        """Проверяет путь до файла"""

        if obj and obj.preview:
            return obj.preview.url
        return None


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории"""

    image = CatalogPreviewSerializer()

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


class SalesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Sales"""

    title = serializers.CharField(source='product.title', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    images = CatalogPreviewSerializer(source='product.images', many=True, read_only=True)

    class Meta:
        model = Sales
        fields = (
            'id',
            'price',
            'title',
            'salePrice',
            'dateFrom',
            'dateTo',
            'images',
        )

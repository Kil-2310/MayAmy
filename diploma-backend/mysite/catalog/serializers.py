from rest_framework import serializers

from .models import (
    Category,
    Subcategory,
    Image,
    Product,
    Tag,
    Sales,
)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов"""

    class Meta:
        model = Tag
        fields = ('id', 'name')

class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор превью"""

    src = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('src', 'alt')

    def get_src(self, obj):
        """Проверяет путь до файла"""

        if obj and obj.preview:
            return obj.preview.url
        return None


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории"""

    image = ImageSerializer()

    class Meta:
        model = Subcategory
        fields = ('id', 'title', 'image')


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категории"""

    image = ImageSerializer()
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')


class CatalogSerializer(serializers.ModelSerializer):
    """Сериализатор для списка товаров"""

    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'rating'
        )


class SalesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Sales"""

    title = serializers.CharField(source='product.title', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    images = ImageSerializer(source='product.images', many=True, read_only=True)

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

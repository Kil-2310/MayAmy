from typing import Union

from rest_framework import serializers

from .models import Product, ProductPreview, Specifications, ProductReviews, Sales
from tags.serializers import TagSerializer


class ProductPreviewSerializer(serializers.ModelSerializer):
    """Сериализатор для картинок продукта"""

    src = serializers.SerializerMethodField()

    class Meta:
        model = ProductPreview
        fields = ('alt', 'src', )

    def get_src(self, obj: ProductPreview) -> Union[str, None]:
        """Проверка пути до изображения"""

        if obj and obj.preview:
            return obj.preview.url
        return None


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для списка товаров"""

    images = ProductPreviewSerializer(many=True)
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
            'rating',
        )


class SpecificationsSerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий продукта"""

    class Meta:
        model = Specifications
        fields = ('name', 'value',)


class GetReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""

    email = serializers.EmailField(source='user.email')
    author = serializers.CharField(source='user.username')

    class Meta:
        model = ProductReviews
        fields = ('author', 'email', 'text', 'rate', 'date', )


class TotalProductSerializer(serializers.ModelSerializer):
    """Сериализатор для списка товаров"""

    images = ProductPreviewSerializer(many=True)
    tags = TagSerializer(many=True)
    specifications = SpecificationsSerializer(many=True)
    reviews = serializers.SerializerMethodField()

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
            'specifications',
            'rating',
        )

    def get_reviews(self, obj: ProductReviews) -> GetReviewsSerializer:
        """Замена поля reviews из модели ProductReviews и получение массива с отзывами вместо него"""

        return GetReviewsSerializer(obj.product_reviews, many=True).data


class CreateReviewSerializer(serializers.Serializer):
    """Сериализатор для создания отзыва"""

    text = serializers.CharField()
    author = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    rate = serializers.FloatField()


class SalesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Sales"""

    title = serializers.CharField(source='product.title')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    images = ProductPreviewSerializer(source='product.images', many=True)

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

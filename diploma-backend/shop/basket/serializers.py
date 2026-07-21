from rest_framework import serializers

from tags.serializers import TagSerializer
from product.serializers import ProductPreviewSerializer
from .models import Basket


class PostBasketSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    count = serializers.IntegerField(required=True, min_value=1)


class GetBasketSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения корзины пользователя"""

    id = serializers.SerializerMethodField()
    category = serializers.CharField(source='product.category')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    date = serializers.DateTimeField(source='product.date')
    title = serializers.CharField(source='product.title')
    description = serializers.CharField(source='product.description')
    freeDelivery = serializers.BooleanField(source='product.freeDelivery')
    images = ProductPreviewSerializer(source='product.images', many=True)
    tags = TagSerializer(source='product.tags', many=True)
    reviews = serializers.IntegerField(source='product.reviews')
    rating = serializers.FloatField(source='product.rating')
    count = serializers.IntegerField(source='quantity')

    class Meta:
        model = Basket
        fields = (
            'id',
            'count',
            'category',
            'price',
            'date',
            'title',
            'description',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'rating',
        )

    def get_id(self, obj: Basket) -> int:
        """Замена id корзмны на id продукта"""
        return obj.product.id

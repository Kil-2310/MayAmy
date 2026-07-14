from rest_framework import serializers

from product.serializers import ProductPreviewSerializer
from tags.serializers import PostTagsSerializer


class CreateOrderSerializer(serializers.Serializer):
    """Сериализатор для списка товаров"""

    id = serializers.IntegerField()
    category = serializers.CharField()
    price = serializers.CharField()
    count = serializers.IntegerField(min_value=1)
    date = serializers.DateTimeField()
    title = serializers.CharField()
    description = serializers.CharField()
    freeDelivery = serializers.BooleanField(default=False)
    reviews = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0.0)
    images = ProductPreviewSerializer(many=True)
    tags = PostTagsSerializer(many=True)


class OrderItemSerializer(serializers.Serializer):
    """Сериализатор для позиции заказа"""

    id = serializers.IntegerField(source='product.id')
    category = serializers.CharField(source='product.category')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    count = serializers.IntegerField()
    date = serializers.DateTimeField(source='product.date')
    title = serializers.CharField(source='product.title')
    description = serializers.CharField(source='product.description')
    freeDelivery = serializers.BooleanField(source='product.freeDelivery')
    reviews = serializers.IntegerField(source='product.reviews')
    rating = serializers.FloatField(source='product.rating')
    images = ProductPreviewSerializer(source='product.images', many=True)
    tags = PostTagsSerializer(source='product.tags', many=True)


class OrderSerializer(serializers.Serializer):
    """Сериализатор для получения заказа"""

    id = serializers.IntegerField(required=False)
    createdAt = serializers.DateTimeField()
    fullName = serializers.CharField(source='profile.fullName')
    email = serializers.EmailField(source='profile.user.email')
    phone = serializers.CharField(source='profile.phone')
    deliveryType = serializers.CharField()
    paymentType = serializers.CharField()
    totalCost = serializers.DecimalField(max_digits=10, decimal_places=2)
    status = serializers.CharField()
    city = serializers.CharField()
    address = serializers.CharField()
    products = OrderItemSerializer(source='order_items', many=True)

from rest_framework import serializers

from .models import Order

# TODO Добавить сериализатор для товаров
class MainOrderSerializer(serializers.ModelSerializer):

    fullName = serializers.CharField(source='profile.fullName')
    email = serializers.EmailField(source='profile.email')
    phone = serializers.CharField(source='profile.phone')

    class Meta:
        model = Order
        fields = (
            'id',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
        )

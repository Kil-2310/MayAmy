from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    """Сериалайзер для оплаты заказов"""

    number = serializers.CharField()
    name = serializers.CharField()
    month = serializers.CharField()
    year = serializers.CharField()
    code = serializers.CharField()

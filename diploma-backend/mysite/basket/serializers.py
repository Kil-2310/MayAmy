from rest_framework import serializers

class BasketSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    count = serializers.IntegerField(required=True)
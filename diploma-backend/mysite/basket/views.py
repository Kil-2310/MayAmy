from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Basket
from catalog.serializers import CatalogSerializer
from catalog.models import Product
from .serializers import BasketSerializer

class BasketView(APIView):
    """CRD операции для корзины"""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['basket'],
        description="Получение корзины",
        responses={
            200: {"description": "Successful operation"},
        }
    )
    def get(self, request: Request) -> Response:
        """Получение корзины"""
        data = Product.objects.filter(basket__user = self.request.user)

        serializer = CatalogSerializer(data, many=True)

        return Response(serializer.data)


    @extend_schema(
        tags=['basket'],
        description="Добавление товара в корзину",
        responses={
            200: {"description": "Successful operation"},
            400: {"description": "Bad Request"},
            404: {"description": "Product not found"},
        },
        request=BasketSerializer,
    )
    @transaction.atomic
    def post(self, request: Request) -> Response:
        """Добавление товара в корзину"""

        serializer = BasketSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        id = serializer.validated_data["id"]
        count = serializer.validated_data["count"]

        product = Product.get_by_id(id=id)

        if count > product.count:
            return Response({
                "message": "The quantity of the product is insufficient"
            })

        product.count -= count

        try:
            basket_item = Basket.objects.get(
                user=self.request.user,
                product=product
            )
            basket_item.count += count
            basket_item.save()
        except ObjectDoesNotExist:
            Basket.objects.create(user=self.request.user, product=product)

        return Response(
            {"message": "Successful operation"}
        )


    @extend_schema(
        tags=['basket'],
        description="Удаление товара из корзины",
        responses={
            200: {"description": "Successful operation"},
            400: {"description": "Bad Request"},
            404: {"description": "Product not found"},
        },
        request=BasketSerializer,
    )
    @transaction.atomic
    def delete(self, request: Request) -> Response:
        """Удаление товара из корзины"""

        serializer = BasketSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        id = serializer.validated_data["id"]
        count = serializer.validated_data["count"]

        product = Product.get_by_id(id=id)

        product.count += count

        basket = get_object_or_404(Basket, product = product, user = self.request.user)
        basket.count -= count

        if basket.count == 0:
            basket.delete()

        product.save()

        return Response(
            {"message": "Successful operation"}
        )

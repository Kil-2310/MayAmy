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
from product.serializers import ProductSerializer
from product.models import Product
from .serializers import BasketSerializer, GetBasketSerializer


class BasketView(APIView):
    """CRD операции для корзины"""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['basket'],
        description="Получение корзины",
        responses={
            200: ProductSerializer(many=True),
        }
    )
    def get(self, request: Request) -> Response:
        """Получение корзины"""
        basket = Basket.objects.filter(user=self.request.user).prefetch_related('product')

        return Response(
            GetBasketSerializer(basket, many=True)
        .data)


    @extend_schema(
        tags=['basket'],
        description="Добавление товара в корзину",
        responses={
            200: ProductSerializer(),
            400: {"description": "Bad Request"},
            404: {"description": "Product not found"},
        },
        request=BasketSerializer,
    )
    @transaction.atomic
    def post(self, request: Request) -> Response:
        """Добавление товара в корзину"""
        request_serializer = BasketSerializer(data=request.data)

        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_id = request_serializer.validated_data["id"]
        count = request_serializer.validated_data["count"]

        product = get_object_or_404(Product, id=product_id)

        if count > product.count:
            return Response({
                "message": "The quantity of the product is insufficient"
            }, status=status.HTTP_400_BAD_REQUEST)

        product.count -= count

        try:
            basket_item = Basket.objects.get(
                user=self.request.user,
                product=product
            )
            basket_item.count += count
            basket_item.save()
        except ObjectDoesNotExist:
            Basket.objects.create(
                user=self.request.user,
                product=product,
                count=count
            )
        finally:
            product.save()

        response_serializer = ProductSerializer(product)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(
        tags=['basket'],
        description="Удаление товара из корзины",
        responses={
            200: ProductSerializer(),
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

        product_id = serializer.validated_data["id"]
        count = serializer.validated_data["count"]

        product = get_object_or_404(Product, id=product_id)
        basket = get_object_or_404(
            Basket,
            product=product,
            user=self.request.user
        )

        if count > basket.count:
            return Response({
                "message": "Cannot remove more items than in basket"
            }, status=status.HTTP_400_BAD_REQUEST)

        product.count += count
        basket.count -= count

        if basket.count == 0:
            basket.delete()
        else:
            basket.save()
        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

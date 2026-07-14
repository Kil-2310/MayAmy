from decimal import Decimal

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, get_list_or_404

from product.models import Product
from .serializers import OrderSerializer
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer


class CreateGetOrder(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['order'],
        description="Получение активного заказа",
        responses={
            200: OrderSerializer(many=True),
            404: {"description": "Not found"},
        },
    )
    def get(self, request: Request) -> Response:
        """Получение активного заказа"""
        order = get_list_or_404(
            Order,
            profile=request.user.profile,
        )

        return Response(
            OrderSerializer(order, many=True).data
        )


    @extend_schema(
        tags=['order'],
        description="Создание нового заказа",
        responses={
            200: {'orderId': 123},
            400: {"description": "bad request"},
            409: {"message": "Conflict"},
        },
        request=CreateOrderSerializer(many=True),
    )
    @transaction.atomic
    def post(self, request: Request) -> Response:
        """Создание нового заказа"""
        serializer = CreateOrderSerializer(data=request.data, many=True)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        profile = self.request.user.profile

        user_order = Order.objects.filter(profile=profile, status='pending').first()

        if user_order:
            user_order.delete()

        total_products = []
        total_cost = Decimal('0.00')

        for product_data in serializer.validated_data:
            user_selected_count = product_data['count']
            product_obj = get_object_or_404(Product, id=product_data['id'])

            if product_obj.count < user_selected_count:
                return Response({
                    "message": f"Not enough stock for product",
                }, status=status.HTTP_409_CONFLICT)

            product_obj.count -= user_selected_count
            product_obj.save()

            product_price = Decimal(str(product_data['price'])) * Decimal(str(product_data['count']))
            total_cost += product_price

            total_products.append({
                'product': product_obj,
                'count': product_data['count'],
                'price': product_data['price']
            })

        new_order = Order.objects.create(
            profile=profile,
            totalCost=total_cost,
        )

        for item_data in total_products:
            OrderItem.objects.create(
                order=new_order,
                product=item_data['product'],
                count=item_data['count'],
                price=item_data['price']
            )

        return Response(
            {'orderId': new_order.pk},
            status=status.HTTP_200_OK
        )


class DetailOrder(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['order'],
        description="Получение конкретного заказа",
        responses={
            200: OrderSerializer(),
            404: {"description": "Not found"},
        },
    )
    def get(self, request: Request, id: int) -> Response:
        """Получение конкретного заказа"""
        order = get_object_or_404(
            Order,
            id=id,
        )

        return Response(
            OrderSerializer(order).data
        )


    @extend_schema(
        tags=['order'],
        description="Подтверждение заказа",
        responses={
            200: {"description": "Successful operation"},
            400: {"message": "Bad request"},
            404: {"description": "Not found"},
        },
        request=OrderSerializer,
    )
    @transaction.atomic
    def post(self, request: Request, id: int) -> Response:
        """Подтверждение заказа"""

        serializer = OrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        order = get_object_or_404(
            Order,
            id=id,
            profile=request.user.profile,
        )

        order.status = 'agreement'
        order.city = serializer.validated_data['city']
        order.address = serializer.validated_data['address']
        order.deliveryType = serializer.validated_data['deliveryType']
        order.paymentType = serializer.validated_data['paymentType']

        order.save()

        return Response(
            {"description": "Successful operation"}
        )

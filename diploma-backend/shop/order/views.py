from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from product.models import Product
from .serializers import MainOrderSerializer
from .models import Order, OrderItem
from product.serializers import ProductSerializer


class CreateGetOrder(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['order'],
        description="Получение активного заказа",
        responses={
            200: MainOrderSerializer(many=True),
        },
    )

    def get(self, request: Request) -> Response:
        """Получение активного заказа"""

        profile = request.user.profile

        order = get_object_or_404(
            Order.objects
            .select_related('profile'),
            profile = profile,
        )

        return Response(
            MainOrderSerializer(order).data
        )

    @extend_schema(
        tags=['order'],
        description="Создание нового заказа",
        responses={
            200: {'orderId': 123},
            400: {"description": "bad request"},
            409: {"message": "Conflict"},
        },
        request=ProductSerializer(many=True),
    )
    def post(self, request: Request) -> Response:
        """Создание нового заказа"""
        serializer = ProductSerializer(data=request.data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order_items_data = []
        total_cost = Decimal('0.00')

        for product_data in serializer.validated_data:
            product_obj = get_object_or_404(Product, id=product_data['id'])

            if product_obj.count < product_data['count']:
                return Response({
                    "message": f"Not enough stock for product",
                }, status=status.HTTP_409_CONFLICT)

            product_obj.count -= product_data['count']
            product_obj.save()

            item_total = Decimal(str(product_data['price'])) * Decimal(str(product_data['count']))
            total_cost += item_total

            order_items_data.append({
                'product': product_obj,
                'count': product_data['count'],
                'price': product_data['price']
            })

        user = request.user

        new_order = Order.objects.create(
            profile=user.profile,
            paymentType='online',
            deliveryType='free',
            totalCost=total_cost,
            city='Moscow',
            address='red square 1',
            status='pending'
        )

        for item_data in order_items_data:
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
            200: MainOrderSerializer(),
        },
    )
    def get(self, request: Request, id: int) -> Response:
        """Получение конкретного заказа"""


    @extend_schema(
        tags=['order'],
        description="Подтверждение заказа",
        responses={
            200: MainOrderSerializer(),
        },
        request=MainOrderSerializer,
    )
    def post(self, request: Request, id: int) -> Response:
        """Подтверждение заказа"""


from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PaymentSerializer
from .models import CreditCard
from order.models import Order
from product.models import Sales
from basket.models import Basket

@extend_schema(
    tags=['payment'],
    description="Оплата заказа",
    request=PaymentSerializer,
    responses={
        200: {"description": "Successful operation"},
        400: {"description": "bad request"},
        404: {"description": "Not found"},
    }
)
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request, id: int) -> Response:
        """Оплата заказа"""

        # Валидация
        serializer = PaymentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        month = int(serializer.validated_data["month"])
        year = int(serializer.validated_data["year"])
        code = serializer.validated_data["code"]
        number = serializer.validated_data["number"]

        # Получение либо создание карты
        profile = self.request.user.profile
        credit_card, created = CreditCard.objects.update_or_create(
            profile=profile,
            defaults={
                'month': month,
                'year': year,
                'code': code,
                'number': number,
            }
        )

        # Закрытие заказа
        order = get_object_or_404(
            Order.objects.prefetch_related('order_items'),
            id=id
        )

        if order.profile != profile:
            return Response(
                {"message": "Access denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        if order.status == 'paid':
            return Response(
                {"message": "Order already paid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'paid'
        order.save()

        # Добавление товаров в таблицу продаж и очистка корзины пользователя
        sales_objects = []

        for item in order.order_items.all():
            product = item.product

            sales_objects.append(
                Sales(
                    product=product,
                    salePrice=item.product.price,
                    dateFrom='05-20',
                    dateTo='05-08',
                )
            )

            Basket.objects.filter(product=product).delete()

        Sales.objects.bulk_create(sales_objects)

        return Response(
            {"description": "Successful operation"}
        )

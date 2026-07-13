from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import MainOrderSerializer
from .models import Order


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
            .select_related('profile', 'products'),
            profile = profile,
        )

        return Response(
            MainOrderSerializer(order).data
        )


    @extend_schema(
        tags=['order'],
        description="Создание нового заказа",
        responses={

        },
    )
    def post(self, request: Request) -> Response:
        """Создание нового заказа"""

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


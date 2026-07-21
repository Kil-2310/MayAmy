from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import ProductReviews, Product
from .serializers import TotalProductSerializer, CreateReviewSerializer, ProductSerializer


@extend_schema(
    tags=['product'],
    description="Получение деталей товара",
    responses={
        200: TotalProductSerializer(),
        404: {"description": "Not found"},
    }
)
class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, id: int) -> Response:
        """Получение деталей товара"""
        product = get_object_or_404(
            Product.objects
            .prefetch_related('tags', 'images', 'product_reviews', 'specifications')
            .select_related('category'),
            id=id
        )

        return Response(
            TotalProductSerializer(product).data
        )


@extend_schema(
    tags=['product'],
    description="Создание отзыва на товар",
    responses={
        200: ProductSerializer(many=True),
        400: {"description": "bad request"},
        404: {"description": "Not found"},
    },
    request=CreateReviewSerializer
)
class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request, id: int) -> Response:
        """Создание отзыва на товар"""
        serializer = CreateReviewSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        text = serializer.validated_data['text']
        rate = Decimal(str(serializer.validated_data['rate']))

        product = get_object_or_404(
            Product.objects.prefetch_related('tags', 'images').select_related('category'),
            id=id
        )

        ProductReviews.objects.create(user=user, text=text, rate=rate, product=product)
        product.reviews += 1

        if product.count == 0:
            product.rating = rate
        else:
            product.rating = (product.rating + rate) / product.count

        product.save()

        reviews = ProductReviews.objects.filter(product=product)

        return Response(
            CreateReviewSerializer(reviews, many=True).data
        )

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import Count

from .serializers import CategoriesSerializer, SalesSerializer
from .models import Category
from product.serializers import ProductSerializer
from product.models import Product, Sales


@extend_schema(
    tags=['catalog'],
    description="Получение вс категорий и подкатегорий",
    responses={
        200: {"description": "Successful operation"},
    }
)
class CategoriesView(APIView):
    """Получение всх категорий и подкатегорий"""

    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        data = Category.objects.all().select_related('image').prefetch_related('subcategories__image')

        return Response(
            CategoriesSerializer(data, many=True)
        .data)


@extend_schema(
    tags=['catalog'],
    description="Получение каталога со всеми товарами",
    responses={
        200: {"description": "Successful operation"},
    }
)
class CatalogView(APIView):
    """Получение каталога со всеми товарами"""

    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        data = Product.objects.all().prefetch_related('images', 'tags')

        return Response(
            {'items': ProductSerializer(data, many=True).data}
        )


@extend_schema(
    tags=['catalog'],
    description="Получение популярных товаров",
    responses={
        200: {"description": "Successful operation"},
    }
)
class ProductsPopularView(APIView):
    """Получение популярных товаров"""
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        data = (
            Product.objects
            .annotate(
                sales_count=Count('sales')
            )
            .order_by('-sales_count')
            .prefetch_related('images')
        )

        return Response(
            ProductSerializer(data, many=True)
        .data)


@extend_schema(
    tags=['catalog'],
    description="Получение лимитированных товаров",
    responses={
        200: {"description": "Successful operation"},
    }
)
class ProductLimitedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """Получение лимитированных товаров"""
        products = Product.objects.filter(isLimited=True).all()

        return Response(
            ProductSerializer(products, many=True)
        .data)


@extend_schema(
    tags=['catalog'],
    description="Получение проданных товаров",
    responses={
        200: {"description": "Successful operation"},
    }
)
class SalesProductView(APIView):
    """Получение проданных товаров"""

    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        data = Sales.objects.all().prefetch_related('product__images')

        return Response(
            {'items': SalesSerializer(data, many=True).data}
        )


@extend_schema(
    tags=['catalog'],
    description="Получение банеров",
    responses={
        200: {"description": "Successful operation"},
    }
)
class BannersView(APIView):
    """Получение банеров"""

    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:

        data = (Product.objects.annotate(
            banner_count=Count('banners')
        )
        .filter(banner_count__gt=0)
        .prefetch_related('tags', 'images'))

        return Response(
            {'items': ProductSerializer(data, many=True).data}
        )

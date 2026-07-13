from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from .models import Category
from product.serializers import ProductSerializer, SalesSerializer
from product.models import Product, Sales
from .filters import ProductFilter, CatalogPagination
from .serializers import MainCategoriesSerializer


@extend_schema(
    tags=['catalog'],
    description="Получение всех категорий и подкатегорий",
    responses={
        200: MainCategoriesSerializer(many=True),
    }
)
class CategoriesView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(cache_page(60 * 2))
    def get(self, request: Request) -> Response:
        """Получение всех категорий и подкатегорий"""
        categories = Category.objects.prefetch_related('subcategories')

        return Response(
            MainCategoriesSerializer(categories, many=True).data
        )


@extend_schema(
    tags=['catalog'],
    description="Получение каталога со всеми товарами",
    responses={
        200: ProductSerializer(many=True),
    }
)
class CatalogView(ReadOnlyModelViewSet):
    """Получение каталога со всеми товарами"""
    permission_classes = [AllowAny]

    serializer_class = ProductSerializer
    pagination_class = CatalogPagination
    queryset = (
        Product.objects
        .prefetch_related('images', 'tags')
        .select_related('category')
    )

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'date', 'reviews', 'rating']

    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(
    tags=['catalog'],
    description="Получение популярных товаров",
    responses={
        200: ProductSerializer(many=True),
    }
)
class ProductsPopularView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """Получение популярных товаров"""
        products = (
            Product.objects
            .annotate(
                sales_count=Count('sales')
            )
            .order_by('-sales_count')
            .prefetch_related('images', 'tags')
            .select_related('category')
        )

        return Response(
            ProductSerializer(products, many=True).data
        )


@extend_schema(
    tags=['catalog'],
    description="Получение лимитированных товаров",
    responses={
        200: ProductSerializer(many=True),
    }
)
class ProductLimitedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """Получение лимитированных товаров"""
        products = (
            Product.objects
            .filter(isLimited=True)
            .prefetch_related('images', 'tags')
            .select_related('category')
        )

        return Response(
            ProductSerializer(products, many=True).data
        )


@extend_schema(
    tags=['catalog'],
    description="Получение проданных товаров",
    responses={
        200: SalesSerializer(many=True),
    }
)
class SalesProductView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """Получение проданных товаров"""
        sales = Sales.objects.select_related('product').prefetch_related('product__images')

        return Response(
            {'items': SalesSerializer(sales, many=True).data}
        )


@extend_schema(
    tags=['catalog'],
    description="Получение банеров",
    responses={
        200: {"description": "Successful operation"},
    }
)
class BannersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """Получение банеров"""
        products = (
            Product.objects
            .filter(banner__isnull=False)
            .prefetch_related('tags', 'images')
            .select_related('category')
        )

        return Response(
            {'items': ProductSerializer(products, many=True).data}
        )

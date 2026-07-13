from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response
from django_filters import FilterSet, NumberFilter, BooleanFilter, CharFilter

from product.models import Product

class CatalogPagination(PageNumberPagination):
    """Класс для модификации ответа"""
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        })


class ProductFilter(FilterSet):
    """Класс для фильтрации"""
    name = CharFilter(field_name='title', lookup_expr='icontains')
    minPrice = NumberFilter(field_name='price', lookup_expr='gte')
    maxPrice = NumberFilter(field_name='price', lookup_expr='lte')
    freeDelivery = BooleanFilter(field_name='freeDelivery')
    available = BooleanFilter(method='filter_available')

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(count__gt=0)
        return queryset

    class Meta:
        model = Product
        fields = ['name', 'minPrice', 'maxPrice', 'freeDelivery', 'available']
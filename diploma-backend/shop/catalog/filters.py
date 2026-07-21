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
    """Класс для точной фильтрации категорий"""
    sort = CharFilter(method='filter_sort')
    sortType = CharFilter(method='filter_sort')

    class Meta:
        model = Product
        fields = []

    def filter_sort(self, queryset, name, value):
        sort_field = self.data.get('sort', '')
        sort_type = self.data.get('sortType', '')

        if not sort_field:
            return queryset

        if sort_type == 'dec':
            sort_field_model = f'-{sort_field}'
        elif sort_type == 'inc':
            sort_field_model = sort_field

        return queryset.order_by(sort_field_model)

    def filter_available_method(self, queryset, name, value):
        if value is True:
            return queryset.filter(
                count__gt=0
            )
        return queryset

    def filter_tags(self, queryset, name, value):
        tags = self.data.getlist('tags[]', '')

        if not tags:
            return queryset

        return queryset.filter(tags__in=[int(tag) for tag in tags])

    @classmethod
    def get_filters(cls):
        filters = super().get_filters()

        filters['filter[name]'] = CharFilter(
            field_name='title',
            lookup_expr='icontains'
        )
        filters['filter[minPrice]'] = NumberFilter(
            field_name='price',
            lookup_expr='gte'
        )
        filters['filter[maxPrice]'] = NumberFilter(
            field_name='price',
            lookup_expr='lte'
        )
        filters['filter[freeDelivery]'] = BooleanFilter(
            field_name='freeDelivery'
        )
        filters['filter[reviews]'] = NumberFilter(
            field_name='reviews',
        )
        filters['filter[available]'] = BooleanFilter(
            method='filter_available_method'
        )
        filters['tags[]'] = NumberFilter(
            method='filter_tags'
        )
        return filters

from django.urls import path

from .views import (
    CategoriesView,
    CatalogView,
    ProductsPopularView,
    ProductLimitedView,
    SalesProductView,
    BannersView,
)


app_name = 'catalog'

urlpatterns = [
    path('categories', CategoriesView.as_view(), name='categories'),
    path('catalog', CatalogView.as_view(), name='catalog'),
    path('products/popular', ProductsPopularView.as_view(), name='products_popular'),
    path('products/limited', ProductLimitedView.as_view(), name='products_limited'),
    path('sales', SalesProductView.as_view(), name='sales_products'),
    path('banners', BannersView.as_view(), name='banners'),
]

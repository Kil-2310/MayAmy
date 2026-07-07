from django.urls import path

from .views import ProductDetailView, CreateReviewView


app_name = 'product'

urlpatterns = [
    path('product/<int:id>', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:id>/reviews', CreateReviewView.as_view(), name='product_detail'),
]

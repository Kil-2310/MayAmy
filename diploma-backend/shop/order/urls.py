from django.urls import path

from .views import CreateGetOrder, DetailOrder


app_name = 'order'

urlpatterns = [
    path('orders', CreateGetOrder.as_view(), name='orders'),
    path('orders/<int:id>/', DetailOrder.as_view(), name='orders_by_id'),
]

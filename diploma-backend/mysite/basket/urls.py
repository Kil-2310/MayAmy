from django.urls import path
from .views import BasketView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('basket/', csrf_exempt(BasketView.as_view()), name='basket'),
]
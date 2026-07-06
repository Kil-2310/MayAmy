from django.urls import path

from .views import LoginView, LogoutView, RegistrationView


app_name = 'myauth'

urlpatterns = [
    path('sign-in', LoginView.as_view(), name='sign_up'),
    path('sign-out', LogoutView.as_view(), name='sign_out'),
    path('sign-up', RegistrationView.as_view(), name='registration'),
]

from django.urls import path, include

from .views import ProfileView, UpdatePasswordView, UpdateAvatarView


app_name = 'user_profile'

urlpatterns = [
    path('profile', ProfileView.as_view(), name='user_profile'),
    path('profile/password', UpdatePasswordView.as_view(), name='update_password'),
    path('profile/avatar', UpdateAvatarView.as_view(), name='update_avatar'),
]

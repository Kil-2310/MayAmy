from django.urls import path

from .views import TagsView


app_name = 'tags'

urlpatterns = [
    path('tags/', TagsView.as_view(), name='tags'),
]

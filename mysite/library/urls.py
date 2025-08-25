from django.urls import path
from .views import index, authors

urlpatterns = [
    path('', index, name='index'),
    path('authors/', authors, name='authors'),
]
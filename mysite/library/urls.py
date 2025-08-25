from django.urls import path
from .views import index, authors, author
from .views import BookListView, BookDetailView

urlpatterns = [
    path('', index, name='index'),
    path('authors/', authors, name='authors'),
    path('authors/<int:author_id>', author, name="author"),
    path('books/', BookListView.as_view(), name='books'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book'),
]
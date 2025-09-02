from django.urls import path
from .views import index, authors, author, search
from .views import BookListView, BookDetailView, UserBookInstanceListView, SignUpView

urlpatterns = [
    path('', index, name='index'),
    path('authors/', authors, name='authors'),
    path('authors/<int:author_id>', author, name="author"),
    path('books/', BookListView.as_view(), name='books'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book'),
    path('search/', search, name='search'),
    path('userinstances/', UserBookInstanceListView.as_view(), name='user_instances'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
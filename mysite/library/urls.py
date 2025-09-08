from django.urls import path
from .views import index, authors, author, search
from .views import (BookListView,
                    BookDetailView,
                    UserBookInstanceListView,
                    ProfileUpdateView,
                    SignUpView,
                    BookInstanceListView,
                    BookInstanceDetailView,
                    BookInstanceCreateView,
                    BookInstanceUpdateView,
                    BookInstanceDeleteView)

urlpatterns = [
    path('', index, name='index'),
    path('authors/', authors, name='authors'),
    path('authors/<int:author_id>', author, name="author"),
    path('books/', BookListView.as_view(), name='books'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book'),
    path('search/', search, name='search'),
    path('userinstances/', UserBookInstanceListView.as_view(), name='user_instances'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileUpdateView.as_view(), name="profile"),
    path('instances/', BookInstanceListView.as_view(), name="instances"),
    path('instances/<int:pk>', BookInstanceDetailView.as_view(), name="instance"),
    path('instances/create', BookInstanceCreateView.as_view(), name='instances_create'),
    path('instances/<int:pk>/update', BookInstanceUpdateView.as_view(), name="instance_update"),
    path('instances/<int:pk>/delete', BookInstanceDeleteView.as_view(), name="instance_delete"),
]
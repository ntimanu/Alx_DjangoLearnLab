from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, BookCreateView, BookUpdateView, BookDeleteView,BookListView, BookSearchView

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)


urlpatterns = [
    path('', include(router.urls)),

    # List all books
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Create a new book
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update an existing book
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete a book
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
    
    # Search books
    path('books/search/', BookSearchView.as_view(), name='book-search'),
]

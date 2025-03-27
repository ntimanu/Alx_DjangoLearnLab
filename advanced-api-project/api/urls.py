from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, BookListView, BookDetailView, BookSearchView

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoint for listing all books and creating a new book
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Endpoint for retrieving, updating, or deleting a specific book
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Endpoint for searching books with advanced filtering
    path('books/search/', BookSearchView.as_view(), name='book-search'),
]
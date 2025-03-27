# api/views.py
from rest_framework import generics, permissions, filters, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter


class BookListView(generics.ListAPIView):
    """
    Comprehensive Book listing view with advanced querying capabilities.
    
    Supports:
    - Filtering by various book attributes
    - Searching across title and author name
    - Ordering by multiple fields
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Enable filtering, searching, and ordering
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # Define the filterset class
    filterset_class = BookFilter
    
    # Configure search fields
    search_fields = [
        'title', 
        'author__name'
    ]
    
    # Define orderable fields
    ordering_fields = [
        'title', 
        'publication_year', 
        'author__name'
    ]
    
    # Default ordering
    ordering = ['-publication_year']
    
    def list(self, request, *args, **kwargs):
        """
        Custom list method to provide additional metadata about the query.
        """
        response = super().list(request, *args, **kwargs)
        
        # Add query metadata to the response
        response.data = {
            'query_params': request.query_params,
            'total_books': self.filter_queryset(self.get_queryset()).count(),
            'results': response.data
        }
        
        return response

class BookSearchView(generics.ListAPIView):
    """
    Advanced Book search view with multiple query capabilities.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Enable filtering, searching, and ordering
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # Define the filterset class
    filterset_class = BookFilter
    
    # Configure search fields
    search_fields = [
        'title', 
        'author__name'
    ]
    
    # Define orderable fields
    ordering_fields = [
        'title', 
        'publication_year', 
        'author__name'
    ]
    
    # Default ordering
    ordering = ['-publication_year']
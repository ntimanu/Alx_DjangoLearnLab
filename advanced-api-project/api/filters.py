import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    Advanced filtering for Book model.
    
    Provides complex filtering options for books.
    """
    # Exact match filtering
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    # Range filtering for publication year
    publication_year = django_filters.NumberFilter()
    publication_year__gt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gt')
    publication_year__lt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lt')
    
    # Filtering by author name
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = [
            'title', 
            'publication_year', 
            'author_name'
        ]
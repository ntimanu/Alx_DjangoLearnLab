from rest_framework import viewsets, generics, permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminOrReadOnly

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Author instances.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookListView(generics.ListCreateAPIView):
    """
    View to list all books or create a new book.
    
    Allows read access to all users, but only authenticated users can create books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def list(self, request):
        """
        Custom list method to add metadata to the response.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'total_books': queryset.count(),
            'books': serializer.data
        })

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific book.
    
    Requires authentication for update and delete operations.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        """
        Custom update method with additional validation and logging.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        # Additional custom validation
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Validation failed', 
                    'details': serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Log the update (in a real-world scenario, use a proper logging framework)
        print(f"Book updated: {instance.title}")
        
        self.perform_update(serializer)
        return Response(serializer.data)

class BookSearchView(generics.ListAPIView):
    """
    Custom view for searching books with additional filtering capabilities.
    """
    serializer_class = BookSerializer
    
    def get_queryset(self):
        """
        Customize queryset based on query parameters.
        
        Supports filtering by author name and publication year range.
        """
        queryset = Book.objects.all()
        
        # Filter by author name (case-insensitive)
        author_name = self.request.query_params.get('author', None)
        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)
        
        # Filter by publication year range
        min_year = self.request.query_params.get('min_year', None)
        max_year = self.request.query_params.get('max_year', None)
        
        if min_year:
            queryset = queryset.filter(publication_year__gte=min_year)
        
        if max_year:
            queryset = queryset.filter(publication_year__lte=max_year)
        
        return queryset

class BookListView(generics.ListCreateAPIView):
    # ... other configurations ...
    permission_classes = [IsAdminOrReadOnly]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    # ... other configurations ...
    permission_classes = [IsAdminOrReadOnly]
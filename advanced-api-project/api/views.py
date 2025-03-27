from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from .models import Book, Author
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter

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

class BookCreateView(generics.CreateAPIView):
    """
    View specifically for creating new Book instances.
    
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method with enhanced error handling and logging.
        """
        serializer = self.get_serializer(data=request.data)
        
        # Additional custom validation
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Book creation failed', 
                    'details': serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Perform the book creation
        self.perform_create(serializer)
        
        # Log the creation (replace with proper logging in production)
        print(f"New book created: {serializer.data.get('title')}")
        
        # Return success response
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

class BookUpdateView(generics.UpdateAPIView):
    """
    View specifically for updating existing Book instances.
    
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        """
        Custom update method with enhanced error handling and validation.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        # Validate the incoming data
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Book update failed', 
                    'details': serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Log the update (replace with proper logging in production)
        print(f"Book updated: {instance.title}")
        
        # Perform the update
        self.perform_update(serializer)
        
        return Response(serializer.data)

class BookDeleteView(generics.DestroyAPIView):
    """
    View specifically for deleting Book instances.
    
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method with logging and additional checks.
        """
        instance = self.get_object()
        
        # Log the deletion (replace with proper logging in production)
        print(f"Book to be deleted: {instance.title}")
        
        # Perform the deletion
        self.perform_destroy(instance)
        
        return Response(
            {
                'message': 'Book successfully deleted', 
                'book_title': instance.title
            }, 
            status=status.HTTP_204_NO_CONTENT
        )

class BookListView(generics.ListAPIView):
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

class BookListView(generics.ListCreateAPIView):
    # ... other configurations ...
    permission_classes = [IsAdminOrReadOnly]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    # ... other configurations ...
    permission_classes = [IsAdminOrReadOnly]
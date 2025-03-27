# api/views.py
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import Book, Author
from .serializers import AuthorSerializer, BookSerializer
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

class BookCreateView(generics.CreateAPIView):
    """
    View specifically for creating new Book instances.
    
    Restricted to admin or authenticated users with write permissions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    
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
    
    Restricted to admin or authenticated users with write permissions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    
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
    
    Restricted to admin or authenticated users with delete permissions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    
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

# Retain the existing search and list views
class BookListView(generics.ListAPIView):
    """
    View to list all books.
    
    Allows read access to all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
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
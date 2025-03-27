from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Book, Author
from .serializers import BookSerializer

class BookAPITestCase(TestCase):
    def setUp(self):
        """
        Set up test environment before each test method.
        This method runs before every individual test, ensuring a clean slate.
        """
        # Create a test client to simulate API requests
        self.client = APIClient()

        # Create a test user for authentication
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )

        # Create a test author
        self.author = Author.objects.create(
            name='Test Author', 
            bio='A test biography'
        )

        # Create some test books
        self.book1 = Book.objects.create(
            title='Test Book 1', 
            author=self.author, 
            publication_year=2020,
            isbn='1234567890'
        )
        self.book2 = Book.objects.create(
            title='Another Test Book', 
            author=self.author, 
            publication_year=2021,
            isbn='0987654321'
        )

        # URLs for different API endpoints
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})

    def test_book_list_unauthenticated(self):
        """
        Test retrieving book list without authentication.
        Verify that unauthenticated users can view the book list.
        """
        response = self.client.get(self.book_list_url)
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if the returned data matches the serializer
        serializer = BookSerializer([self.book1, self.book2], many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_book_create_authenticated(self):
        """
        Test book creation by an authenticated user.
        Verify that authenticated users can create books.
        """
        # Authenticate the test user
        self.client.force_authenticate(user=self.user)

        # Prepare book data for creation
        book_data = {
            'title': 'New Test Book',
            'author': self.author.pk,
            'publication_year': 2022,
            'isbn': '1122334455'
        }

        # Send POST request to create a book
        response = self.client.post(self.book_list_url, book_data)

        # Check if book creation is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the book was actually created in the database
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())

    def test_book_create_unauthenticated(self):
        """
        Test book creation without authentication.
        Verify that unauthenticated users cannot create books.
        """
        book_data = {
            'title': 'Unauthorized Book',
            'author': self.author.pk,
            'publication_year': 2022,
            'isbn': '5566778899'
        }

        # Try to create a book without authentication
        response = self.client.post(self.book_list_url, book_data)

        # Check if creation is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_update_authenticated(self):
        """
        Test book update by an authenticated user.
        Verify that authenticated users can update existing books.
        """
        # Authenticate the test user
        self.client.force_authenticate(user=self.user)

        # Prepare updated book data
        updated_data = {
            'title': 'Updated Test Book',
            'author': self.author.pk,
            'publication_year': 2023,
            'isbn': self.book1.isbn
        }

        # Send PUT request to update the book
        response = self.client.put(self.book_detail_url, updated_data)

        # Check if update is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the book from the database
        self.book1.refresh_from_db()
        
        # Verify the book was actually updated
        self.assertEqual(self.book1.title, 'Updated Test Book')
        self.assertEqual(self.book1.publication_year, 2023)

    def test_book_delete_authenticated(self):
        """
        Test book deletion by an authenticated user.
        Verify that authenticated users can delete books.
        """
        # Authenticate the test user
        self.client.force_authenticate(user=self.user)

        # Send DELETE request to remove the book
        response = self.client.delete(self.book_detail_url)

        # Check if deletion is successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the book was actually deleted from the database
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_book_filtering(self):
        """
        Test API filtering functionality.
        Verify that filtering by various attributes works correctly.
        """
        # Test filtering by publication year
        response = self.client.get(f'{self.book_list_url}?publication_year=2020')
        
        # Check if filtering works
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')

    def test_book_search(self):
        """
        Test API search functionality.
        Verify that searching by title works correctly.
        """
        # Test searching for a book by partial title
        response = self.client.get(f'{self.book_list_url}?search=Test')
        
        # Check if search works
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)

    def test_book_ordering(self):
        """
        Test API ordering functionality.
        Verify that ordering by publication year works correctly.
        """
        # Test ordering by publication year in descending order
        response = self.client.get(f'{self.book_list_url}?ordering=-publication_year')
        
        # Check if ordering works
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Another Test Book')
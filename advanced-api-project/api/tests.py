from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Book, Author
from .serializers import BookSerializer

# Configure a separate test database
TEST_DATABASES = settings.DATABASES.copy()
TEST_DATABASES['default']['NAME'] = 'test_advanced_api_project'

@override_settings(DATABASES=TEST_DATABASES)
class BookAPITestCase(APITestCase):
    """
    Comprehensive test suite for Book API endpoints
    Uses a separate test database to avoid impacting production data
    """

    def setUp(self):
        """
        Set up test environment before each test method.
        Creates test data and authentication credentials.
        """
        # Create test client
        self.client = APIClient()

        # Create test user for authentication
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpassword123'
        )

        # Create test author
        self.author = Author.objects.create(
            name='Test Author',
            bio='Sample author biography'
        )

        # Create test books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            author=self.author,
            publication_year=2020,
            isbn='1234567890'
        )
        self.book2 = Book.objects.create(
            title='Test Book 2',
            author=self.author,
            publication_year=2021,
            isbn='0987654321'
        )

        # URLs for API endpoints
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})

    def test_book_list_get(self):
        """
        Test retrieving the list of books
        Verify correct status code and response content
        """
        response = self.client.get(self.list_url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify response contains correct number of books
        self.assertEqual(len(response.data['results']), 2)

    def test_book_create_authenticated(self):
        """
        Test book creation by authenticated user
        Verify correct status codes for successful creation
        """
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Prepare book data
        book_data = {
            'title': 'New Test Book',
            'author': self.author.pk,
            'publication_year': 2022,
            'isbn': '5555555555'
        }

        # Send POST request
        response = self.client.post(self.list_url, book_data)
        
        # Check status code for successful creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify book was created in database
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())

    def test_book_create_unauthenticated(self):
        """
        Test book creation by unauthenticated user
        Verify unauthorized access is prevented
        """
        book_data = {
            'title': 'Unauthorized Book',
            'author': self.author.pk,
            'publication_year': 2022,
            'isbn': '6666666666'
        }

        # Send POST request without authentication
        response = self.client.post(self.list_url, book_data)
        
        # Check unauthorized status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_update(self):
        """
        Test book update by authenticated user
        Verify correct status codes and data modification
        """
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Prepare update data
        update_data = {
            'title': 'Updated Book Title',
            'author': self.author.pk,
            'publication_year': 2023,
            'isbn': self.book1.isbn
        }

        # Send PUT request
        response = self.client.put(self.detail_url, update_data)
        
        # Check status code for successful update
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh book from database and verify changes
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')

    def test_book_delete(self):
        """
        Test book deletion by authenticated user
        Verify correct status codes and database changes
        """
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Send DELETE request
        response = self.client.delete(self.detail_url)
        
        # Check status code for successful deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify book was removed from database
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_book_filtering(self):
        """
        Test API filtering functionality
        Verify correct filtering by publication year
        """
        # Send filtered request
        response = self.client.get(f'{self.list_url}?publication_year=2020')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify correct number of filtered results
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')
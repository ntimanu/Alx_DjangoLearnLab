from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):

    def setUp(self):
        """
        Setup test data before each test runs.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create an author
        self.author = Author.objects.create(name="John Doe", bio="Test Author Bio")
        
        # Create a book instance
        self.book = Book.objects.create(title="Test Book", author=self.author, publication_year=2020)
        
        # Define API endpoints
        self.book_list_url = reverse('book-list')  # Ensure this matches your urlpatterns
        self.book_detail_url = reverse('book-detail', args=[self.book.id])

    def test_create_book(self):
        """
        Test creating a new book via API.
        """
        # Authenticate the test client
        self.client.login(username='testuser', password='testpass')

        data = {"title": "New Book", "author": self.author.id, "publication_year": 2021}
        response = self.client.post(self.book_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.latest('id').title, "New Book")

    def test_list_books(self):
        """
        Test retrieving a list of books.
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_book(self):
        """
        Test retrieving a single book.
        """
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        """
        Test updating a book via API.
        """
        # Authenticate the test client
        self.client.login(username='testuser', password='testpass')

        updated_data = {"title": "Updated Book Title", "author": self.author.id, "publication_year": 2022}
        response = self.client.put(self.book_detail_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book Title")

    def test_delete_book(self):
        """
        Test deleting a book via API.
        """
        # Authenticate the test client
        self.client.login(username='testuser', password='testpass')

        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_search_books_by_author(self):
        """
        Test searching books by author name.
        """
        search_url = f"{self.book_list_url}?search=John"
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_permission_restrictions(self):
        """
        Ensure unauthenticated users cannot create, update, or delete books.
        """
        # Logout to remove authentication
        self.client.logout()

        # Test book creation
        response = self.client.post(self.book_list_url, {
            "title": "Unauthorized Book", 
            "author": self.author.id, 
            "publication_year": 2021
        })
        # Expect Forbidden (403) instead of Unauthorized (401)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test book update
        response = self.client.put(self.book_detail_url, {
            "title": "Unauthorized Update", 
            "author": self.author.id, 
            "publication_year": 2022
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test book deletion
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
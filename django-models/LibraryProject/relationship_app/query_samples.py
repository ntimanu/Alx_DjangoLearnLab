# relationship_app\query_sample.py

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def books_by_author(author_name):
    books = Book.objects.filter(author__name=author_name)
    return [book.title for book in books]

# List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return [book.title for book in library.books.all()]

# Retrieve the librarian for a library
def librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian.name
    except Librarian.DoesNotExist:
        return "No librarian assigned."

# Sample test cases
if __name__ == "__main__":
    print("Books by Author 'John Doe':", books_by_author('John Doe'))
    print("Books in Library 'Central Library':", books_in_library('Central Library'))
    print("Librarian of 'Central Library':", librarian_for_library('Central Library'))

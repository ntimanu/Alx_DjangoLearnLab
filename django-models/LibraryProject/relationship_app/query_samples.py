# relationship_app\query_samples.py

import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')  # Adjust if your project name is different
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        # Use objects.filter instead of accessing through the related_name
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []

def list_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}:")
        for book in books:
            print(f"- {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []

def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(name=library_name)
        try:
            # Use Librarian.objects.get(library=library) instead of library.librarian
            librarian = Librarian.objects.get(library=library)
            print(f"The librarian for {library_name} is {librarian.name}.")
            return librarian
        except Librarian.DoesNotExist:
            print(f"No librarian assigned to {library_name}.")
            return None
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
   
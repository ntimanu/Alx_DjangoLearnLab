# relationship_app\query_sample.py

import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []

def books_in_library(library_name):
    """List all books in a specific library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}:")
        for book in books:
            print(f"-{book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []

def librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    
    try:
        librarian = librarian.objects.get(library=library)
        print(f"The librarian for {library_name} is {librarian.name}.")
        return librarian
    except Librarian.DoesNotExist:
        print(f"No Librarian assigned to {library_name}.")
        return None
    
    

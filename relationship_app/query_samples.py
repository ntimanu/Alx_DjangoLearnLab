<<<<<<< HEAD
# relationship_app\query_samples.py

import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')  # Adjust if your project name is different
=======
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
>>>>>>> 322e5fd575c4677913c3bed629c19f9a742cb34f
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

<<<<<<< HEAD
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
   
=======
# Query 1: Get all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.filter(name=author_name).first()
    if author:
        books = Book.objects.filter(author=author)
        return [book.title for book in books]
    return []

# Query 2: List all books in a specific library
def get_books_in_library(library_name):
    library = Library.objects.filter(name=library_name).first()
    if library:
        books = library.books.all()
        return [book.title for book in books]
    return []

# Query 3: Retrieve the librarian of a specific library
def get_librarian_for_library(library_name):
    library = Library.objects.filter(name=library_name).first()
    if library:
        librarian = Librarian.objects.filter(library=library).first()
        return librarian.name if librarian else "No librarian assigned"
    return "Library not found"

# Example Usage
if __name__ == "__main__":
    print(get_books_by_author("J.K. Rowling"))
    print(get_books_in_library("Central Library"))
    print(get_librarian_for_library("Central Library"))
>>>>>>> 322e5fd575c4677913c3bed629c19f9a742cb34f

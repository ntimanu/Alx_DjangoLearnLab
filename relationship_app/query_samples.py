import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

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

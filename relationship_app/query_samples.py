# query_samples.py

from relationship_app.models import Author, Book, Librarian

# Query: List all books in a library
def list_books_in_library():
    books = Book.objects.all()
    for book in books:
        print(book.title)

# Query: Query all books by a specific author
def query_books_by_author(author_name):
    author = Author.objects.filter(name=author_name).first()
    books = Book.objects.filter(author=author)
    for book in books:
        print(book.title)

# Query: Retrieve the librarian for a library
def retrieve_librarian(library_name):
    librarian = Librarian.objects.filter(library_name=library_name).first()
    print(librarian.name)

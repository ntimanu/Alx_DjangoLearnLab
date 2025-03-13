
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden
from .models import Book
from django.shortcuts import render
from bookshelf.models import Book
from bookshelf.forms import BookSearchForm  # Import the secure form

# View all books (Requires 'can_view' permission)
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Create a book (Requires 'can_create' permission)
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        published_date = request.POST['published_date']
        Book.objects.create(title=title, author=author, published_date=published_date)
        return redirect('book_list')
    return render(request, 'bookshelf/book_form.html')

# Edit a book (Requires 'can_edit' permission)
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.published_date = request.POST['published_date']
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_form.html', {'book': book})

# Delete a book (Requires 'can_delete' permission)
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')

def search_books(request):
    """
    Securely searches books by title.
    - Uses Django ORM to prevent SQL injection.
    - Strips user input to avoid unnecessary spaces.
    - Uses Django forms for validation.
    """
    form = BookSearchForm(request.GET)
    books = []
    if form.is_valid():
        title = form.cleaned_data["title"]
        books = Book.objects.filter(title__icontains=title)  # ✅ Secure query
    return render(request, "bookshelf/book_list.html", {"form": form, "books": books})

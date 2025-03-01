from django.shortcuts import render, redirect
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views 

# Class-Based View to show details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Helper functions for role-based access control
def is_admin(user):
    return user.is_authenticated and hasattr(user, "userprofile") and user.userprofile.role == "Admin"

def is_librarian(user):
    return user.is_authenticated and hasattr(user, "userprofile") and user.userprofile.role == "Librarian"

def is_member(user):
    return user.is_authenticated and hasattr(user, "userprofile") and user.userprofile.role == "Member"

# Admin view (only accessible by Admins)
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

# Librarian view (only accessible by Librarians)
@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

# Member view (only accessible by Members)
@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # User Authentication URLs - Using class-based views
    path("register/", views.register_view, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Admin, Librarian, and Member views
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),

    # Book Management URLs (Adding, Editing, Deleting books)
    path('add_book/', views.add_book, name='add_book'),  
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),  
    path('book/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]
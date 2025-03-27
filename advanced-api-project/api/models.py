# api/models.py
from django.db import models
from django.utils import timezone

class Author(models.Model):
    """
    Author model to store information about book authors.
    
    This model has a one-to-many relationship with the Book model,
    allowing one author to have multiple books.
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model to store information about books.
    
    Each book is associated with exactly one author via a ForeignKey relationship,
    establishing a many-to-one relationship from Book to Author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        related_name='books'  # This allows us to access books via author.books
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
# api/models.py
from django.db import models
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        related_name='books'  # This allows us to access books via author.books
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
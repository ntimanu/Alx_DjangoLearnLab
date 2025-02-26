from django.db import models

# Athor Model
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
# Book Model with a ForeignKey to Author
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
    
#Library Model with ManyToManyField to Book
class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name
    
#Librarian Model with OneToOneField to library
class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name

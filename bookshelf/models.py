from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
<<<<<<< HEAD
        return f"{self.title} by {self.author} {self.publication_year}"
=======
        return f"{self.title} by {self.author} {self.publication_year}."
>>>>>>> 322e5fd575c4677913c3bed629c19f9a742cb34f

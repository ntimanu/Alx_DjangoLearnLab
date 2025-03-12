from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from .models import Author, Book, Library, Librarian

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
>>>>>>> 322e5fd575c4677913c3bed629c19f9a742cb34f

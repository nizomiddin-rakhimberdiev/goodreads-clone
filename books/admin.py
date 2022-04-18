from django.contrib import admin

# Register your models here.
from books.models import Genre, Book, Author, BookAuthor, BookReview, GenreBook, GenreAuthor, Rating


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')


class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreBook)
admin.site.register(GenreAuthor)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor)
admin.site.register(BookReview)
admin.site.register(Rating)

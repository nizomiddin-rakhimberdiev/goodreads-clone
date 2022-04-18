from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from users.models import CustomUser


# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    cover_picture = models.ImageField(default='default_cover_pic.png')

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    info_birth = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    personal_photo = models.ImageField(default='default_profile_pic.png')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} by {self.author.first_name} {self.author.last_name}"


class GenreBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} in the genre {self.genre.name}"


class GenreAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.first_name} {self.author.last_name}'s genre is {self.genre.name}"


class BookReview(models.Model):
    comment = models.TextField()
    stars_given = models.IntegerField(default=0,
                                      validators=[MinValueValidator(0), MaxValueValidator(5)]
                                      )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Rated {self.stars_given} stars by {self.user.username}"


class Rating(models.Model):
    image = models.ImageField()
    stars_given = models.IntegerField(default=0,
                                      validators=[MinValueValidator(0), MaxValueValidator(5)]
                                      )

    def __str__(self):
        return str(self.pk)

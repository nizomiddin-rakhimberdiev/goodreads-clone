from rest_framework import serializers

from books.models import Book, BookReview
from users.models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn', 'cover_picture')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'profile_picture')

class BookReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    book_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = BookReview
        fields = ('id', 'stars_given', 'comment', 'book', 'user', 'book_id', 'user_id')
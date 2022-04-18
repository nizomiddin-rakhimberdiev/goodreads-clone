from django import forms

from books.models import BookReview, Author


class BookReviewsForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=0, max_value=5)
    
    class Meta:
        model = BookReview
        fields = ('stars_given','comment')


class BookAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name','info_birth', 'email', 'personal_photo')
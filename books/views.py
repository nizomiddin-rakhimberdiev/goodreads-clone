from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from books.forms import BookReviewsForm, BookAuthorForm
from books.models import Book, Genre, BookReview, Author, BookAuthor
from users.models import CustomUser


class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)
        page_size = request.GET.get('page_size', 4)
        paginator = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        return render(request, 'books/list.html', {'page_obj':page_obj})

class BookDetailView(View):
    def get(self, request, id, user_id):
        user = CustomUser.objects.get(id=user_id)
        book = Book.objects.get(id=id)
        return render(request, 'books/detail.html', {'book': book, 'user': user})



class AddReviewView(LoginRequiredMixin, View):

    def get(self, request, book_id):
        book = Book.objects.get(id=book_id)
        review_form = BookReviewsForm()
        return render(request, 'books/review.html', {'book':book, 'review_form':review_form,})

    def post(self, request, book_id):
        book = Book.objects.get(id=book_id)
        review_form = BookReviewsForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )
            return redirect(reverse('books:detail', kwargs={'id':book.id}))
        return render(request, 'books/review.html', {'book': book, 'review_form': review_form})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_form = BookReviewsForm(instance=review)

        return render(request, 'books/edit_review.html', {
            'book': book,
            'review': review,
            'review_form': review_form
        })

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)
        review_form = BookReviewsForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={'id':book.id}) )
        return render(request, 'books/edit_review.html', {
            'book': book,
            'review': review,
            'review_form': review_form
        })

class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)

        return render(request, 'books/confirm_delete_review.html', {'book': book, 'review': review})

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = BookReview.objects.get(id=review_id)

        review.delete()
        messages.success(request, "You have successfully deleted this review.")
        return redirect(reverse('books:detail', kwargs={'id':book.id}))


class BookAuthorView(View):
    def get(self, request, book_id, author_id):
        books = Book.objects.all().order_by('id')
        book = Book.objects.get(id=book_id)
        book_author = BookAuthor.objects.get(id=author_id)
        return render(request, 'books/author.html', {'book': book, 'book_author': book_author, 'books':books},)

class UsersProfileView(View):
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        return render(request, 'books/user_profile.html', {'user': user})



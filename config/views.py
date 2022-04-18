from django.core.paginator import Paginator
from django.http import request
from django.shortcuts import render

from books.models import BookReview, Book, Rating


def landing_page(request):
    # obj = Rating.objects.filter(stars_given=0).order_by("?").first()
    book = Book.objects.get(id=2)
    reviews = BookReview.objects.all().order_by('-created_at')
    if request.user.is_authenticated:
        return render(request, 'landing.html', {'book':book, 'reviews':reviews})
    else:
        return render(request, 'default.html')


def home_page(request):
    reviews = BookReview.objects.all().order_by('-created_at')

    page_size = request.GET.get('page_size', 2)
    paginator = Paginator(reviews, page_size)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    return render(request, 'home.html', {'page_obj': page_obj})

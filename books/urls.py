from django.urls import path

from books.views import BookDetailView, BookListView, AddReviewView, EditReviewView, ConfirmDeleteReviewView, \
    DeleteReviewView, BookAuthorView, UsersProfileView

app_name= 'books'
urlpatterns = [
    path('list/', BookListView.as_view(), name='list'),
    path('<int:id>/', BookDetailView.as_view(), name='detail'),
    path('<int:book_id>/review/', AddReviewView.as_view(), name='review'),
    path('<int:book_id>/review/<int:review_id>/edit/', EditReviewView.as_view(), name='edit-review'),
    path('<int:book_id>/review/<int:review_id>/confirm-delete/', ConfirmDeleteReviewView.as_view(), name='c-delete-review'),
    path('<int:book_id>/review/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete-review'),
    path('<int:book_id>/author/<int:author_id>/', BookAuthorView.as_view(), name='author'),
    path('user/<int:id>/', UsersProfileView.as_view(), name='user-profile'),

]
from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Book', description='Description', isbn='1111111')
        user = CustomUser.objects.create(
            username='nizomiddin',
            first_name='Nizomiddin',
            last_name="Rakhimberdiev",
            email='nizomiddinoff@mail.ru',
        )
        user.set_password('somepass')
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment='Nice book')
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment='Great book')
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment='Good book')

        response = self.client.get(reverse('home_page') + '?page_size=2')

        self.assertContains(response, review2.comment)
        self.assertContains(response, review3.comment)
        self.assertNotContains(response, review1.comment)
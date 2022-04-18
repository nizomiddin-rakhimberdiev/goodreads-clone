from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from books.models import Book, Author
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, "No books found.")

    def test_book_list(self):
        book1 = Book.objects.create(title='Book1', description='Description1', isbn='11111')
        book2 = Book.objects.create(title='Book2', description='Description2', isbn='22222')
        book3 = Book.objects.create(title='Book3', description='Description3', isbn='33333')

        response = self.client.get(reverse('books:list') + '?page_size=2')

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?page=2&page_size=2')

        self.assertContains(response, book3.title)

    def test_book_detail(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='11111')

        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, book.isbn)
        self.assertContains(response, book.full_name)

    def test_search_list(self):
        book1 = Book.objects.create(title='Sport', description='description1', isbn='11111')
        book2 = Book.objects.create(title='Deep Work', description='description2', isbn='22222')
        book3 = Book.objects.create(title='Shoe Dog', description='description3', isbn='33333')

        response = self.client.get(reverse('books:list', ) + '?q=sport')
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list', ) + '?q=deep')
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list', ) + '?q=shoe')
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        user = CustomUser.objects.create(
            username='nizomiddin', first_name='Nizomiddin', last_name="Rakhimberdiev", email='nizomiddinoff@mail.ru',
        )
        user.set_password('somepass')
        user.save()

        book = Book.objects.create(title='Book1', description='Description1', isbn='12345678')

        self.client.login(username='nizomiddin', password='somepass')

        self.client.post(reverse("books:reviews", kwargs={'id': book.id}), data={
            "stars_given": 3,
            'comment': 'Nice book'
        })

        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'Nice book')
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)


class BookAuthorDetailTestCase(TestCase):
    def test_book_author_detail(self):
        book = Book.objects.create(title='Sport', description='description1', isbn='11111')
        author = Author.objects.create(first_name='Author', last_name='Author_l_name', info_birth='US 1976',
                                       email='author@gmail.com')

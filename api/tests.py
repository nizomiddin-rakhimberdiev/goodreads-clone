from django.test import TestCase

# Create your tests here.
from rest_framework.reverse import reverse

from books.models import Book, BookReview
from rest_framework.test import APITestCase

from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='nizomiddin', first_name='Nizomiddin')
        self.user.set_password('somepass')
        self.user.save()
        self.client.login(username='nizomiddin', password='somepass')


    def test_review_detail(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='11111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Very good book')

        response = self.client.get(reverse('api:review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], 'Very good book')
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], br.book.title)
        self.assertEqual(response.data['book']['description'], br.book.description)
        self.assertEqual(response.data['book']['isbn'], br.book.isbn)
        self.assertEqual(response.data['user']['id'], br.user.id)
        self.assertEqual(response.data['user']['first_name'], br.user.first_name)
        self.assertEqual(response.data['user']['username'], br.user.username)

    def test_delete_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='11111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Very good book')

        response = self.client.delete(reverse('api:review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())


    def test_patch_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='11111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Very good book')

        response = self.client.patch(reverse('api:review-detail', kwargs={'id': br.id}), data={'stars_given': 4})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)


    def test_put_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='11111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='Very good book')

        response = self.client.patch(reverse('api:review-detail', kwargs={'id': br.id}),
                                     data={'stars_given': 4, 'comment': 'nice book', 'user_id': self.user.id,
                                           'book_id': book.id})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'nice book')

    def test_create_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='11111')
        data = {
            'stars_given': 4,
            'comment': 'nice book',
            'user_id': self.user.id,
            'book_id': book.id
        }
        response = self.client.post(reverse('api:review-list'), data=data)
        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'nice book')
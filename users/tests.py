from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from users.models import CustomUser


class USerRegisterTestCase(TestCase):
    def test_user_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                'username':'nizomiddin',
                'first_name':'Nizomiddin',
                'last_name':'Rakhimberdiev',
                'email':'nizomiddinoff@mail.ru',
                'password':'somepass',
            }
        )

        user = CustomUser.objects.get(username='nizomiddin')

        self.assertEqual(user.first_name, 'Nizomiddin')
        self.assertEqual(user.last_name, 'Rakhimberdiev')
        self.assertEqual(user.email, 'nizomiddinoff@mail.ru')
        self.assertNotEqual(user.password, 'somepass')
        self.assertTrue(user.check_password, 'somepass')

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'Nizomiddin',
                'email': 'nizomddinoff@mail.ru'
            }
        )
        user_count = CustomUser.objects.count()
        
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'nizomiddin',
                'first_name': 'Nizomiddin',
                'last_name': 'Rakhimberdiev',
                'email': 'invalid_email',
                'password': 'somepass',
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        user = CustomUser.objects.create(username='nizomiddin', first_name='Nizomiddin')
        user.set_password('somepass')
        user.save()

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'nizomiddin',
                'first_name': 'Nizomiddin',
                'last_name': 'Rakhimberdiev',
                'email': 'invalid_email',
                'password': 'somepass',
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEquals(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


    def test_login_required(self):  # bu test user login bo'lganligini tekshiradi
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')


    def test_profile_detail(self):
        user = CustomUser.objects.create(
            username='nizomiddin', last_name="Rakhimberdiev", email='nizomiddinoff@mail.ru',
        )
        user.set_password('somepass')
        user.save()

        self.client.login(username='nizomiddin', password='somepass')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username='nizomiddin', first_name='Nizomiddin', last_name="Rakhimberdiev", email='nizomiddinoff@mail.ru',
        )
        user.set_password('somepass')
        user.save()

        self.client.login(username='nizomiddin', password='somepass')

        response = self.client.post(
            reverse('users:edit-profile'),
            data={
                'username': 'nizomiddin',
                'first_name': 'Nizomiddin',
                'last_name': 'Rahimberdiyev',
                'email': 'nizomiddinoff@gmail.com'
            }
        )

        user.refresh_from_db()
        self.assertEqual(user.last_name, 'Rahimberdiyev')
        self.assertEqual(user.email, 'nizomiddinoff@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))
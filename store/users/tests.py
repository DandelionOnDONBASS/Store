from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now

from users.forms import UserLoginForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'first_name': 'qwerty',
            'last_name': 'qwerty123',
            'username': 'qwerty1234',
            'email': 'qwerty123qwe@erty.com',
            'password1': '12345678qwezxC',
            'password2': '12345678qwezxC',
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):

        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username = username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        username = self.data['username']
        user = User.objects.create(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
        


    def test_user_login(self):
        path = reverse('users:login')
        response = self.client.get(path)
        register_user = self.client.post(self.path, self.data)
        form = response.context['form']

        self.assertIn('form', response.context)
        self.assertIsInstance(form, UserLoginForm)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        data_user = {'username': 'qwerty1234', 'password': '12345678qwezxC'}
        responsess = self.client.post(path, data_user)
        self.assertEqual(responsess.status_code, HTTPStatus.FOUND)
        self.assertRedirects(responsess, '/')




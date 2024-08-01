from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from documents.models import User
from django.urls import reverse


class UserCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:user_create')

    def test_create_user(self):
        """
        Тестирование создания пользователя через UserCreateAPIView.
        Проверка установки пароля и правильного ответа.
        """
        data = {
            'email': 'testuser@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=data['email'])
        self.assertTrue(user.check_password(data['password']))
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
from django.contrib.auth.models import Group, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from documents.models import Document
from documents.serializers import DocumentSerializer
from users.models import User
from rest_framework.serializers import ValidationError


class DocumentViewSetTestCase(APITestCase):
    """
    Тесты для проверки работы DocumentViewSet.
    """

    def setUp(self):
        """
        Настройка данных перед запуском тестов.
        Создаем пользователей с разными правами и несколько документов.
        """
        self.group_admin = Group.objects.create(name='Document Administrators')

        self.view_permission = Permission.objects.get(codename='view_document')
        self.change_permission = Permission.objects.get(codename='change_document')
        self.add_permission = Permission.objects.get(codename='add_document')

        self.group_admin.permissions.add(self.view_permission, self.change_permission)

        self.user = User.objects.create(email='user@example.com', password='password')
        self.user1 = User.objects.create(email='user1@example.com', password='password')
        self.user1.groups.add(self.group_admin)

        file1 = SimpleUploadedFile("file1.pdf", b"file_content", content_type="application/pdf")
        file2 = SimpleUploadedFile("file2.pdf", b"file_content", content_type="application/pdf")

        self.document1 = Document.objects.create(owner=self.user, file=file1, status='в обработке')
        self.document2 = Document.objects.create(owner=self.user1, file=file2, status='принят')

    def test_create_document_as_unauthenticated_user(self):
        """
        Тестирование создания документа неавторизованным пользователем.
        Ожидаем, что ответ будет статусом 401 Unauthorized.
        """
        url = reverse('documents:document-list')
        test_file = SimpleUploadedFile("file3.pdf", b"file_content", content_type="application/pdf")

        data = {
            'file': test_file,
            'status': 'в обработке'
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Document.objects.count(), 2)

    def test_create_document_as_authenticated_user(self):
        """
        Тестирование создания документа авторизованным пользователем.
        Ожидаем, что ответ будет статусом 201 Created и документ будет создан.
        """

        self.client.force_authenticate(user=self.user1)
        url = reverse('documents:document-list')

        test_file = SimpleUploadedFile("file3.pdf", b"file_content", content_type="application/pdf")

        data = {
            'file': test_file,
            'status': 'в обработке'
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_documents_as_authorized_user(self):
        """
        Тестирование получения списка документов авторизованным пользователем.
        Ожидаем, что ответ будет статусом 403 Forbidden.
        """
        url = reverse('documents:document-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_documents_admins(self):
        """
        Тестирование получения списка документов авторизованным пользователем,
        который является администратором.
        Ожидаем, что ответ будет статусом 200 OK.
        """
        url = reverse('documents:document-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_documents_unauthenticated_user(self):
        """
        Тестирование получения списка документов неавторизованным пользователем.
        Ожидаем, что ответ будет статусом 401 Unauthorized.
        """
        url = reverse('documents:document-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_document_as_authorized_user(self):
        """
        Тестирование обновление документов авторизованным пользователем.
        Ожидаем, что ответ будет статусом 403 Forbidden.
        """
        url = reverse('documents:document-detail', kwargs={'pk': self.document1.id})
        self.client.force_authenticate(user=self.user)
        data = {
            'status': 'отклонен'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_document_as_admin(self):
        """
        Тестирование обновление документов администратором.
        Ожидаем, что ответ будет статусом 200 OK.
        """
        url = reverse('documents:document-detail', kwargs={'pk': self.document1.id})
        self.client.force_authenticate(user=self.user1)
        data = {
            'status': 'отклонен'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_document_as_unauthenticated_user(self):
        """
        Тестирование обновления документа неавторизованным пользователем.
        Ожидаем, что ответ будет статусом 401 Unauthorized.
        """
        url = reverse('documents:document-detail', kwargs={'pk': self.document1.id})

        data = {
            'status': 'отклонен'
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_document_as_admin(self):
        """
        Тестирование удаления документа администратором.
        Ожидаем, что ответ будет статусом 204 No Content, и документ будет удален.
        """
        url = reverse('documents:document-detail', kwargs={'pk': self.document1.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Document.objects.filter(id=self.document1.id).exists())

    def test_delete_document_as_unauthenticated_user(self):
        """
        Тестирование удаления документа неавторизованным пользователем.
        Ожидаем, что ответ будет статусом 401 Unauthorized.
        """
        url = reverse('documents:document-detail', kwargs={'pk': self.document1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_document_as_authorized_user(self):
        """
        Тестирование удаления документа авторизованным пользователем.
        Ожидаем, что ответ будет статусом 403 Forbidden.
        """
        url = reverse('documents:document-detail', kwargs={'pk': self.document1.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FileTypeValidatorTestCase(APITestCase):
    def test_valid_file(self):
        """
        Тестирование обработки валидного файла.
        """
        valid_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        data = {'file': valid_file}
        serializer = DocumentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_extension(self):
        """
        Тестирование обработки файла с недопустимым расширением.
        """
        invalid_file = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
        data = {'file': invalid_file}
        serializer = DocumentSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

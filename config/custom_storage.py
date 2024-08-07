from storages.backends.s3boto3 import S3Boto3Storage
import uuid
import os
from django.conf import settings


class CustomS3Boto3Storage(S3Boto3Storage):
    """
    Кастомное хранилище для S3, которое генерирует уникальные имена файлов
    и возвращает корректные публичные URL.
    """

    def _save(self, name, content):
        """
        Переопределяем метод для генерации уникального имени файла.
        """
        base, extension = os.path.splitext(name)
        unique_name = f"{base}_{uuid.uuid4().hex}{extension}"
        return super()._save(unique_name, content)

    def url(self, name, parameters=None, expire=None):
        """
        Переопределяем метод для возвращения публичного URL.
        """

        original_url = super().url(name, parameters, expire)
        public_url = f'http://{os.getenv("MINIO_STORAGE_ENDPOINT_PUBLIC")}'
        relative_path = original_url.split(os.getenv("MINIO_STORAGE_ENDPOINT"))[-1]
        return f'{public_url.rstrip("/")}{relative_path}'


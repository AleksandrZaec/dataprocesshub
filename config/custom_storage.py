from storages.backends.s3boto3 import S3Boto3Storage
import uuid
import os


class CustomS3Boto3Storage(S3Boto3Storage):
    """
    Кастомное хранилище для S3, которое генерирует уникальные имена файлов.
    """
    def _save(self, name, content):
        """
        Переопределяем метод для генерации уникального имени файла.
        """
        base, extension = os.path.splitext(name)
        unique_name = f"{base}_{uuid.uuid4().hex}{extension}"
        return super()._save(unique_name, content)

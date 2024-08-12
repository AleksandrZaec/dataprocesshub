from django.conf import settings
import boto3
from documents.tasks import send_document_creation_email_task
from django.urls import reverse


def send_document_creation_email(document, request):
    """
    Отправляет email уведомление о создании нового документа через Celery.
    """
    request_url = request.build_absolute_uri(reverse('admin:documents_document_change', args=[document.id]))
    send_document_creation_email_task.delay(document.id, request_url)


def delete_from_storage(file_name):
    """
      Удаляет файл из облачного хранилища по-заданному имени.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL
    )

    try:
        s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_name)
        print(f"Successfully deleted file: {file_name}")
    except Exception as e:
        print(f"Error deleting file: {e}")


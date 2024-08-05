from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_document_status_email(user_id, document_id, status, comment=None):
    """
        Отправляет email уведомление пользователю о статусе его документа.
    """
    from users.models import User
    from documents.models import Document

    user = User.objects.get(id=user_id)
    document = Document.objects.get(id=document_id)

    subject = 'Статус вашего документа'
    message = f'Здравствуйте, {user.first_name}!\n\nВаш документ был {status}.'
    if status == 'отклонен' and comment:
        message += f'\n\nПричина отклонения: {comment}'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,)

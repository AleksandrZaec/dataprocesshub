from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from documents.models import Document


@shared_task
def get_admin_emails(group_name='Document Administrators'):
    """
    Возвращает список email адресов администраторов из указанной группы.
    """
    try:
        group = Group.objects.get(name=group_name)
        return [user.email for user in group.user_set.filter(mailing=True)]
    except Group.DoesNotExist:
        return []


def send_document_creation_email_task(document_id, request_url):
    """
    Асинхронная задача для отправки email уведомления о создании нового документа.
    """
    document = Document.objects.get(id=document_id)
    subject = 'Новый документ создан'
    message = (
        f"Пользователь {document.owner.email} создал новый документ.\n\n"
        f"Детали документа:\n"
        f"Имя файла: {document.file.name}\n"
        f"Статус: {document.status}\n"
        f"Время загрузки: {document.uploaded_at}\n\n"
        f"Просмотреть документ: {request_url}"
    )

    admin_emails = [user.email for user in
                    Group.objects.get(name='Document Administrators').user_set.filter(mailing=True)]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        admin_emails,
        fail_silently=False,
    )


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
        fail_silently=False, )

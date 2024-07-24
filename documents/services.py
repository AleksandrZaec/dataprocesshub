from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Group


def get_admin_emails(group_name='Document Administrators'):
    try:
        group = Group.objects.get(name=group_name)
        return [user.email for user in group.user_set.all()]
    except Group.DoesNotExist:
        return []


def send_document_creation_email(document, request):
    subject = 'Новый документ создан'
    message = (
        f"Пользователь {document.owner.email} создал новый документ.\n\n"
        f"Детали документа:\n"
        f"Имя файла: {document.file.name}\n"
        f"Статус: {document.status}\n"
        f"Время загрузки: {document.uploaded_at}\n\n"
        f"Просмотреть документ: {request.build_absolute_uri(reverse('admin:documents_document_change', args=[document.id]))}"
    )
    admin_emails = get_admin_emails()
    if admin_emails:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            admin_emails,
            fail_silently=False,
        )


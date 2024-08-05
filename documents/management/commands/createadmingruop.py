from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from documents.permissions import get_document_permissions


class Command(BaseCommand):
    """
      Команда для создания группы "Document Administrators" с правами на просмотр и изменение документов,
      а также назначение разрешения на создание документов для всех авторизованных пользователей.
    """
    help = 'Создание группы с правами на просмотр и изменение документа для администраторов, а также разрешение на создание документа для авторизованных пользователей'

    def handle(self, *args, **kwargs):

        view_permission, change_permission, add_permission = get_document_permissions()

        group_name = 'Document Administrators'
        group, created = Group.objects.get_or_create(name=group_name)

        if view_permission:
            group.permissions.add(view_permission)
        if change_permission:
            group.permissions.add(change_permission)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" успешно создана и права назначены.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" уже существует и права назначены.'))

        if add_permission:
            self.stdout.write(self.style.SUCCESS(
                f'Разрешение "{add_permission.name}" доступно для всех авторизованных пользователей.'))
        else:
            self.stdout.write(self.style.WARNING('Разрешение на создание документов не найдено.'))

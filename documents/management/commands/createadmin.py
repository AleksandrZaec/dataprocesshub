from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from documents.permissions import get_document_permissions

User = get_user_model()


class Command(BaseCommand):
    help = 'Создание админа с заданным email и паролем'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email суперпользователя')
        parser.add_argument('--password', type=str, help='Пароль суперпользователя')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']

        if not email or not password:
            self.stdout.write(self.style.ERROR('Email и пароль обязательны.'))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'Пользователь с email "{email}" уже существует.'))
            return

        user = User.objects.create(email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Администратор с email "{email}" успешно создан.'))

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

        # Добавляем пользователя в группу
        user.groups.add(group)
        self.stdout.write(
            self.style.SUCCESS(f'Пользователь с email "{email}" успешно добавлен в группу "{group_name}".'))

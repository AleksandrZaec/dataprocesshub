from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import User


class Command(BaseCommand):
    help = 'Добавление зарегистрированного пользователя по email в группу Document Administrators и предоставление доступа к админке'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str,
                            help='Email пользователя для добавления в группу Document Administrators')

    def handle(self, *args, **kwargs):
        email = kwargs['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Пользователь с email "{email}" не найден.'))
            return

        group_name = 'Document Administrators'
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Группа "{group_name}" не найдена.'))
            return

        if not user.is_staff:
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Пользователю с email "{email}" предоставлен доступ к админке.'))

        if user in group.user_set.all():
            self.stdout.write(
                self.style.WARNING(f'Пользователь с email "{email}" уже является членом группы "{group_name}".'))
        else:
            user.groups.add(group)
            self.stdout.write(
                self.style.SUCCESS(f'Пользователь с email "{email}" успешно добавлен в группу "{group_name}".'))

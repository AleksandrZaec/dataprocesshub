# Generated by Django 5.0.7 on 2024-07-24 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mailing',
            field=models.BooleanField(default=True, verbose_name='Уведомлять администратора'),
        ),
    ]

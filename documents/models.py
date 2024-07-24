from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Document(models.Model):
    STATUS_CHOICES = [
        ('в обработке', 'В обработке'),
        ('принят', 'Принят'),
        ('отклонен', 'Отклонен'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='отправитель')
    file = models.FileField(upload_to='documents/', verbose_name='документ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='в обработке',
                              verbose_name='Статус документа')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Время доставки')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f"{self.file.name} - {self.status}"

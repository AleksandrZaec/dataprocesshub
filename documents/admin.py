from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from documents.forms import RejectionCommentForm
from documents.models import Document
from django.utils.safestring import mark_safe
from documents.services import delete_from_storage
from documents.tasks import send_document_status_email
from django.urls import reverse


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
       Административный интерфейс для модели Document.
       Позволяет администратору просматривать, фильтровать и выполнять действия с документами.
    """
    list_display = ('file', 'owner_details', 'status', 'uploaded_at', 'rejection_comment')
    list_filter = ('status', 'owner')
    actions = ['approve_documents', 'reject_documents']

    # def get_queryset(self, request):
    #     """
    #     Ограничивает отображаемые документы только теми, у которых статус "в обработке".
    #     """
    #     qs = super().get_queryset(request)
    #     if not request.user.is_superuser:
    #         qs = qs.filter(status='в обработке')
    #     return qs

    def delete_queryset(self, request, queryset):
        """
        Удаляет документы из базы данных и облачного хранилища.
        """
        for obj in queryset:
            if obj.file:
                delete_from_storage(obj.file.name)
        super().delete_queryset(request, queryset)

    def owner_details(self, obj):
        """
               Отображает подробности о владельце документа.
        """
        owner = obj.owner
        return mark_safe(
            f"Email: {owner.email}<br>"
            f"Имя: {owner.first_name}<br>"
            f"Фамилия: {owner.last_name}<br>"
            f"Дата регистрации: {owner.date_joined}<br>"
            f"Телефон: {getattr(owner, 'phone', 'не указано')}<br>"
            f"Город: {getattr(owner, 'city', 'не указано')}"
        )

    owner_details.short_description = "Детали пользователя"

    def approve_documents(self, request, queryset):
        """
                Одобряет выбранные документы и отправляет уведомление о статусе.
        """
        for document in queryset:
            send_document_status_email.delay(document.owner.id, document.id, 'принят', None)
        queryset.update(status='принят', rejection_comment='')
        self.message_user(request, "Документы приняты.")

    approve_documents.short_description = "Принять документы"

    def reject_documents(self, request, queryset):
        """
                Перенаправляет на кастомный URL для отклонения документов с комментариями.
        """
        selected_ids = queryset.values_list('id', flat=True)
        return HttpResponseRedirect(
            f"{reverse('admin:reject_documents')}?ids={','.join(map(str, selected_ids))}"
        )

    reject_documents.short_description = "Отклонить документы"

    def get_urls(self):
        """
                Возвращает список URL-адресов для кастомных страниц в админке.
        """
        urls = super().get_urls()
        custom_urls = [
            path('reject-documents/', self.admin_site.admin_view(self.reject_documents_view), name='reject_documents'),
        ]
        return custom_urls + urls

    def reject_documents_view(self, request):
        """
                Обрабатывает страницу для отклонения документов и отображает форму для комментария.
        """
        ids = request.GET.get('ids', '').split(',')
        queryset = Document.objects.filter(id__in=ids)
        if request.method == 'POST':
            form = RejectionCommentForm(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['rejection_comment']
                for document in queryset:
                    if document.file:
                        delete_from_storage(document.file.name)
                        document.file.delete()

                    send_document_status_email.delay(document.owner.id, document.id, 'отклонен', comment)
                queryset.update(status='отклонен', rejection_comment=comment)
                self.message_user(request, "Документы отклонены с комментариями.")
                return HttpResponseRedirect(reverse('admin:documents_document_changelist'))
            else:
                return render(request, 'admin/reject_documents.html', {'form': form})
        else:
            form = RejectionCommentForm()

        return render(request, 'admin/reject_documents.html', {'form': form})

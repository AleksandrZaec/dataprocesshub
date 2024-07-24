from django.contrib import admin
from .models import Document
from django.utils.safestring import mark_safe

from .tasks import send_document_status_email


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('file', 'owner_details', 'status', 'uploaded_at')
    list_filter = ('status', 'owner')
    actions = ['approve_documents', 'reject_documents']

    def owner_details(self, obj):
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
        for document in queryset:
            send_document_status_email.delay(document.owner.id, document.id, 'принят')
        queryset.update(status='принят')

    approve_documents.short_description = "Принять документ"

    def reject_documents(self, request, queryset):
        for document in queryset:
            send_document_status_email.delay(document.owner.id, document.id, 'отклонен')
        queryset.update(status='отклонен')

    reject_documents.short_description = "Отклонить документ"

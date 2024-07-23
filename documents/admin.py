from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'status', 'uploaded_at')
    list_filter = ('status', 'user')
    actions = ['approve_documents', 'reject_documents']

    def approve_documents(self, request, queryset):
        queryset.update(status='принят')

    approve_documents.short_description = "Принять документ"

    def reject_documents(self, request, queryset):
        queryset.update(status='отклонен')

    reject_documents.short_description = "Отклонить документ"


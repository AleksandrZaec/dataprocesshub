from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from documents.models import Document
from documents.permissions import IsAdminGroupOrSuperuserOrReadOnly
from documents.serializers import DocumentSerializer
from documents.tasks import send_document_creation_email


class DocumentViewSet(viewsets.ModelViewSet):
    """
       ViewSet для управления документами. Позволяет создавать, обновлять, удалять и просматривать документы.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsAdminGroupOrSuperuserOrReadOnly]

    def perform_create(self, serializer):
        """
            Сохраняет документ и отправляет email-уведомление.
        """
        document = serializer.save(owner=self.request.user, status='в обработке')
        request_url = self.request.build_absolute_uri(reverse('admin:documents_document_change', args=[document.id]))
        send_document_creation_email.delay(document.id, request_url)

    def create(self, request, *args, **kwargs):
        """
            Обрабатывает создание нового документа и возвращает кастомное сообщение.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'Ваш документ успешно загружен'}, status=status.HTTP_201_CREATED)

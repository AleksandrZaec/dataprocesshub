from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from documents.models import Document
from documents.permissions import IsAdminGroupOrSuperuserOrReadOnly
from documents.serializers import DocumentSerializer
from documents.services import send_document_creation_email


class DocumentViewSet(viewsets.ModelViewSet):
    """
       ViewSet для управления документами. Позволяет создавать, обновлять, удалять и просматривать документы.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsAdminGroupOrSuperuserOrReadOnly]

    def perform_create(self, serializer):
        document = serializer.save(owner=self.request.user, status='в обработке')
        send_document_creation_email(document, self.request)


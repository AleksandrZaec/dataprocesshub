from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from documents.models import Document
from documents.permissions import IsAdminGroupOrSuperuserOrReadOnly
from documents.serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsAdminGroupOrSuperuserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='в обработке')

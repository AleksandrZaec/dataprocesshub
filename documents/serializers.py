from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from documents.models import Document
from documents.validators import FileTypeValidator


class DocumentSerializer(ModelSerializer):
    file = serializers.FileField(validators=[FileTypeValidator()])

    class Meta:
        model = Document
        fields = ['id', 'file']

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Document
from .validators import FileTypeValidator


class DocumentSerializer(ModelSerializer):
    file = serializers.FileField(validators=[FileTypeValidator()])

    class Meta:
        model = Document
        fields = ['id', 'file']

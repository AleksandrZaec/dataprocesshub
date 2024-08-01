import mimetypes
from rest_framework.serializers import ValidationError

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'tif', 'tiff'}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'image/png',
    'image/jpeg',
    'image/tiff'
}


class FileTypeValidator:
    def __call__(self, file):
        extension = file.name.split('.')[-1].lower()
        mime_type, _ = mimetypes.guess_type(file.name)

        if extension not in ALLOWED_EXTENSIONS:
            raise ValidationError("Неподдерживаемое расширение файла")

        if mime_type not in ALLOWED_MIME_TYPES:
            raise ValidationError("Неподдерживаемый тип файла")

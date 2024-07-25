from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions
from documents.models import Document


class IsAdminGroupOrSuperuserOrReadOnly(permissions.BasePermission):
    """
    Разрешить просмотр и изменение только пользователям из группы Document Administrators и суперпользователям.
    Разрешить создание документов всем авторизованным пользователям.
    """

    def has_permission(self, request, view):

        if view.action == 'create' and request.user.is_authenticated:
            return True

        if request.user.is_authenticated and (
                request.user.is_superuser or request.user.groups.filter(name='Document Administrators').exists()
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated and (
                request.user.is_superuser or request.user.groups.filter(name='Document Administrators').exists()
        ):
            return True
        return False


def get_document_permissions():
    """
    Возвращает объекты разрешений для модели Document.
    Использует стандартные разрешения Django.
    """
    content_type = ContentType.objects.get_for_model(Document)

    try:
        # Используйте стандартные коды разрешений
        view_permission = Permission.objects.get(codename='view_document', content_type=content_type)
    except Permission.DoesNotExist:
        view_permission = None

    try:
        change_permission = Permission.objects.get(codename='change_document', content_type=content_type)
    except Permission.DoesNotExist:
        change_permission = None

    try:
        add_permission = Permission.objects.get(codename='add_document', content_type=content_type)
    except Permission.DoesNotExist:
        add_permission = None

    return view_permission, change_permission, add_permission

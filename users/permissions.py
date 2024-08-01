from rest_framework import permissions


class IsSuperuserOrOwner(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только владельцам объекта или суперпользователю.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj == request.user


class IsSuperuser(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только суперпользователям.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только суперпользователям или пользователям, состоящим в группе 'Document Administrators'.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Document Administrators').exists():
            return True
        return False


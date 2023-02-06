from rest_framework.permissions import (SAFE_METHODS,
                                        IsAuthenticatedOrReadOnly,
                                        BasePermission)


class IsAdminOrReadOnly(BasePermission):
    """Полный доступ администратор. Остальные только чтение."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdmin(BasePermission):
    """Администратор."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminModeratorOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Администратор, модератор, автор или только для чтения.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (not request.user.is_anonymous and (
                request.user.is_admin or request.user.is_moderator
                or obj.author == request.user))
        )

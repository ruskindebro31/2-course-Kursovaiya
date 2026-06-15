from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение: только владелец может редактировать/удалять.
    Все могут просматривать.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS — разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для write-операций — только владелец
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'profile'):
            return obj.profile.user == request.user

        # Для User/Profile без связи — владелец
        if isinstance(obj, type(request.user)):
            return obj == request.user

        return False

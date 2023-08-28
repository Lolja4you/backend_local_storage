from rest_framework import permissions
from rest_framework.response import Response

class IsAuthenticatedModeratorAndAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверка на авторизацию пользователя
        if not request.user.is_authenticated:
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        # Проверка на авторство записи
        if obj.media_user != request.user:
            Response('Error: 501. U are not authorized!')
            return False
        
        return True
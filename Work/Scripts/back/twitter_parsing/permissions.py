from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Цель: Здесь создается новый фильтр
    Автор: Немашкало Александр
    """
    def has_object_permission(self,request,view,obj):
        """
        Цель: Ограничить доступ пользователей к записям в бд, которые они не создавали
        Вход:self,  request , view ,obj
        Выход: true /false
        Автор: Немашкало Александр
        """
        return obj.user == request.user


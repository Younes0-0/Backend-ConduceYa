# 📌 Explicación:
# ✅ EsAdmin → Solo los administradores (is_staff=True) pueden usar ciertos endpoints.
# ✅ EsProfesor → Solo los usuarios que sean profesores pueden acceder a sus horarios.

from rest_framework import permissions

class EsAdmin(permissions.BasePermission):
    """Permiso que permite acceso solo a administradores"""
    def has_permission(self, request, view):
        return request.user.is_staff  # Solo admin puede acceder

class EsProfesor(permissions.BasePermission):
    """Permite acceso solo a profesores para sus propios horarios"""
    def has_permission(self, request, view):
        return hasattr(request.user, 'profesor')  # Verifica si el usuario es un profesor

class EsProfesorDueño(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj puede ser una ClasePractica, HorarioDisponible, etc.
        return hasattr(request.user, 'profesor') and obj.profesor == request.user.profesor
# usuarios/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User, Profesor, Alumno
from .serializers import UserSerializer, ProfesorSerializer, AlumnoSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD de usuarios.
    • Admins: alta/baja/edición y listado completo.
    • Endpoint extra /users/yo/ para que cualquier usuario vea su propio perfil.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # ← por defecto solo admins
    permission_classes = [permissions.IsAdminUser]

    # --- Permisos por acción -------------------------------------------- #
    def get_permissions(self):
        # El endpoint "yo" es de solo lectura para el propio usuario
        if self.action == "yo":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    # --- Acción “yo” ----------------------------------------------------- #
    @action(detail=False, methods=["get"], url_path="yo")
    def yo(self, request):
        """
        Devuelve el propio usuario autenticado con un campo extra 'rol'.
        """
        user = request.user
        rol = (
            "admin" if user.is_staff else
            "profesor" if hasattr(user, "profesor") else
            "alumno"
        )
        data = self.get_serializer(user).data | {"rol": rol}
        return Response(data)


class ProfesorViewSet(viewsets.ModelViewSet):
    """Perfiles de profesores – solo administradores."""
    queryset = Profesor.objects.select_related("usuario")
    serializer_class = ProfesorSerializer
    permission_classes = [permissions.IsAdminUser]


class AlumnoViewSet(viewsets.ModelViewSet):
    """Perfiles de alumnos – solo administradores."""
    queryset = Alumno.objects.select_related("usuario")
    serializer_class = AlumnoSerializer
    permission_classes = [permissions.IsAdminUser]

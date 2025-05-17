from rest_framework import viewsets, permissions
from .models import User, Profesor, Alumno
from .serializers import UserSerializer, ProfesorSerializer, AlumnoSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para usuarios.
    Listar, crear, actualizar y eliminar usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class ProfesorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para perfiles de profesores.
    Solo administradores pueden manipular perfiles.
    """
    queryset = Profesor.objects.select_related('usuario').all()
    serializer_class = ProfesorSerializer
    permission_classes = [permissions.IsAdminUser]


class AlumnoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para perfiles de alumnos.
    Solo administradores pueden manipular perfiles.
    """
    queryset = Alumno.objects.select_related('usuario').all()
    serializer_class = AlumnoSerializer
    permission_classes = [permissions.IsAdminUser]


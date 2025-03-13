from rest_framework import viewsets, permissions
from .models import Profesor, HorarioDisponible, ClasePractica
from .serializers import ProfesorSerializer, HorarioDisponibleSerializer, ClasePracticaSerializer
from .permissions import EsAdmin, EsProfesor  # Importamos los permisos personalizados

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    permission_classes = [EsAdmin]  # Solo los administradores pueden gestionar profesores

class HorarioDisponibleViewSet(viewsets.ModelViewSet):
    serializer_class = HorarioDisponibleSerializer
    permission_classes = [EsProfesor | EsAdmin]  # Solo profesores y admins pueden ver horarios
    queryset = HorarioDisponible.objects.all()  # 🔥 SE AGREGA EL QUERYSET

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profesor'):
            return HorarioDisponible.objects.filter(profesor=user.profesor)  # Filtra horarios del profesor
        return HorarioDisponible.objects.none()  # Si no es profesor, no ve nada

class ClasePracticaViewSet(viewsets.ModelViewSet):
    serializer_class = ClasePracticaSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados
    queryset = ClasePractica.objects.all()  # 🔥 SE AGREGA EL QUERYSET

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Admin puede ver todas las clases
            return ClasePractica.objects.all()
        return ClasePractica.objects.filter(alumno=user)  # Los alumnos solo ven sus propias reservas

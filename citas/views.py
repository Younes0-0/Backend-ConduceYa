from rest_framework import viewsets, permissions
from .models import Profesor, HorarioDisponible, ClasePractica
from .serializers import ProfesorSerializer, HorarioDisponibleSerializer, ClasePracticaSerializer
from .permissions import EsAdmin, EsProfesor
from citas import serializers  # Importamos los permisos personalizados

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    permission_classes = [EsAdmin]  # Solo los administradores pueden gestionar profesores

class HorarioDisponibleViewSet(viewsets.ModelViewSet):
    serializer_class = HorarioDisponibleSerializer
    permission_classes = [EsProfesor | EsAdmin]
    queryset = HorarioDisponible.objects.all()

    def get_queryset(self):
        user = self.request.user
    
        if user.is_staff:  # 🔥 Si es admin, ve todos los horarios
            return HorarioDisponible.objects.all()
        
        elif hasattr(user, 'profesor'):  # 🔥 Si es profesor, solo ve sus propios horarios
            return HorarioDisponible.objects.filter(profesor=user.profesor)
        
        else:  # 🔥 Si es un usuario normal (alumno), ve todos los horarios disponibles
            return HorarioDisponible.objects.exclude(id__in=ClasePractica.objects.values_list('horario', flat=True))  # Excluye los ocupados

    def perform_create(self, serializer):
        """🔥 Asigna el profesor correctamente al crear un horario"""
        if hasattr(self.request.user, 'profesor'):
            profesor = self.request.user.profesor  # Obtiene la instancia de Profesor
            serializer.save(profesor=profesor)  # Asigna el profesor
        else:
            raise serializers.ValidationError("Solo los profesores pueden crear horarios.")

class ClasePracticaViewSet(viewsets.ModelViewSet):
    serializer_class = ClasePracticaSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados
    queryset = ClasePractica.objects.all()  # 🔥 SE AGREGA EL QUERYSET

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Admin puede ver todas las clases
            return ClasePractica.objects.all()
        return ClasePractica.objects.filter(alumno=user)  # Los alumnos solo ven sus propias reservas

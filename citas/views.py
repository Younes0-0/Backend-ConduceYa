from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Profesor, HorarioDisponible, ClasePractica
from .serializers import ProfesorSerializer, HorarioDisponibleSerializer, ClasePracticaSerializer
from .permissions import EsAdmin, EsProfesor, EsProfesorDueño

User = get_user_model()

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    permission_classes = [EsAdmin]  # Solo los administradores pueden gestionar profesores

class HorarioDisponibleViewSet(viewsets.ModelViewSet):
    queryset = HorarioDisponible.objects.all()
    serializer_class = HorarioDisponibleSerializer
    permission_classes = [EsProfesor | IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        if hasattr(user, 'profesor'):
            return super().get_queryset().filter(profesor=user.profesor)
        # Alumnos: solo ve horarios libres
        return super().get_queryset().exclude(
            id__in=ClasePractica.objects.values_list('horario', flat=True)
        )

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'profesor'):
            serializer.save(profesor=self.request.user.profesor)
        else:
            from rest_framework import serializers
            raise serializers.ValidationError("Solo los profesores pueden crear horarios.")

class ClasePracticaViewSet(viewsets.ModelViewSet):
    queryset = ClasePractica.objects.select_related('alumno', 'horario__profesor').all()
    serializer_class = ClasePracticaSerializer
    permission_classes = [IsAuthenticated, EsProfesorDueño | IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        if hasattr(user, 'profesor'):
            return super().get_queryset().filter(horario__profesor=user.profesor)
        return super().get_queryset().filter(alumno=user)

    def create(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Use el endpoint /citas/agendar/ para reservar una clase.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {'detail': 'No permitido. Use endpoints específicos para modificar citas.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Use el endpoint /citas/cancelar/<cita_id>/ para cancelar una cita.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    rol = (
        "admin" if user.is_staff else
        "profesor" if hasattr(user, "profesor") else
        "alumno"
    )
    return Response({"username": user.username, "rol": rol})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agendar_cita(request):
    horario_id = request.data.get('horario_id')
    if not horario_id:
        return Response({"error": "Se requiere el ID del horario"}, status=status.HTTP_400_BAD_REQUEST)
    horario = get_object_or_404(HorarioDisponible, id=horario_id)
    if ClasePractica.objects.filter(horario=horario).exists():
        return Response({"error": "Este horario ya está reservado"}, status=status.HTTP_400_BAD_REQUEST)
    if hasattr(request.user, 'profesor') and horario.profesor == request.user.profesor:
        return Response({"error": "No puedes agendar con tu propio horario."}, status=status.HTTP_400_BAD_REQUEST)
    clase = ClasePractica.objects.create(alumno=request.user, horario=horario)
    serializer = ClasePracticaSerializer(clase)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(ClasePractica, id=cita_id)
    user = request.user
    if not (user.is_staff or cita.alumno == user or (hasattr(user, 'profesor') and cita.horario.profesor == user.profesor)):
        return Response({"error": "No tienes permiso para cancelar esta cita."}, status=status.HTTP_403_FORBIDDEN)
    cita.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_disponibilidad(request):
    horarios_disponibles = HorarioDisponible.objects.exclude(
        id__in=ClasePractica.objects.values_list('horario', flat=True)
    )
    serializer = HorarioDisponibleSerializer(horarios_disponibles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_citas(request):
    user = request.user
    if user.is_staff:
        citas = ClasePractica.objects.select_related('alumno', 'horario__profesor').all()
    elif hasattr(user, 'profesor'):
        citas = ClasePractica.objects.select_related('alumno', 'horario').filter(horario__profesor=user.profesor)
    else:
        citas = ClasePractica.objects.select_related('horario__profesor').filter(alumno=user)
    serializer = ClasePracticaSerializer(citas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def listar_usuarios(request):
    usuarios = User.objects.all()
    datos = []
    for u in usuarios:
        rol = (
            "admin" if u.is_staff else
            "profesor" if hasattr(u, "profesor") else
            "alumno"
        )
        datos.append({"id": u.id, "username": u.username, "email": u.email, "rol": rol})
    return Response(datos)
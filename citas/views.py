from rest_framework import viewsets, permissions
from .models import Profesor, HorarioDisponible, ClasePractica
from .serializers import ProfesorSerializer, HorarioDisponibleSerializer, ClasePracticaSerializer
from .permissions import EsAdmin, EsProfesor
from citas import serializers  # Importamos los permisos personalizados
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework import status
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    rol = "admin" if user.is_staff else "profesor" if hasattr(user, "profesor") else "alumno"

    return Response({
        "username": user.username,
        "rol": rol
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agendar_cita(request):
    horario_id = request.data.get('horario_id')

    if not horario_id:
        return Response({"error": "Se requiere el ID del horario"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        horario = HorarioDisponible.objects.get(id=horario_id)
    except HorarioDisponible.DoesNotExist:
        return Response({"error": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Verifica que el horario no esté ocupado
    if ClasePractica.objects.filter(horario=horario).exists():
        return Response({"error": "Este horario ya está reservado"}, status=status.HTTP_400_BAD_REQUEST)

    # Crea la clase práctica
    clase = ClasePractica.objects.create(
        alumno=request.user,
        horario=horario
    )

    serializer = ClasePracticaSerializer(clase)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancelar_cita(request, cita_id):
    try:
        cita = ClasePractica.objects.get(id=cita_id)
    except ClasePractica.DoesNotExist:
        return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.user != cita.alumno and not request.user.is_staff:
        return Response({"error": "No tienes permiso para cancelar esta cita"}, status=status.HTTP_403_FORBIDDEN)

    cita.delete()
    return Response({"message": "Cita cancelada exitosamente"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_disponibilidad(request):
    horarios_ocupados = ClasePractica.objects.values_list('horario_id', flat=True)
    horarios_disponibles = HorarioDisponible.objects.exclude(id__in=horarios_ocupados)

    serializer = HorarioDisponibleSerializer(horarios_disponibles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_citas(request):
    user = request.user

    if user.is_staff:
        citas = ClasePractica.objects.all()
    else:
        citas = ClasePractica.objects.filter(alumno=user)

    serializer = ClasePracticaSerializer(citas, many=True)
    return Response(serializer.data)



User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAdminUser])
def listar_usuarios(request):
    usuarios = User.objects.all()
    datos = []

    for user in usuarios:
        rol = "admin" if user.is_staff else "profesor" if hasattr(user, "profesor") else "alumno"
        datos.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "rol": rol
        })

    return Response(datos, status=status.HTTP_200_OK)

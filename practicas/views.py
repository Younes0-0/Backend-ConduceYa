from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Zona, Solicitud, SalidaDisponible, Reserva
from .serializers import (
    ZonaSerializer, SolicitudSerializer,
    SalidaDisponibleSerializer, ReservaSerializer
)
from citas.models import Profesor


class ZonaViewSet(viewsets.ModelViewSet):
    """CRUD de Zonas (solo admin)"""
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    permission_classes = [permissions.IsAdminUser]


class SolicitudViewSet(viewsets.ModelViewSet):
    """Gestión de solicitudes por zona y sesión"""
    queryset = Solicitud.objects.all().order_by('fecha_inscripcion')
    serializer_class = SolicitudSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Solo admins y profesores pueden listar o modificar
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        # Cualquier usuario autenticado puede crear
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def invitar(self, request, pk=None):
        """Marcar solicitud como invitada (I) y generar Reserva"""
        solicitud = self.get_object()
        solicitud.estado = 'I'
        solicitud.save()
        # Crear reserva pendiente a partir de solicitud
        # Aquí asumiríamos seleccionar una SalidaDisponible de contexto
        return Response({'status': 'invitado'}, status=status.HTTP_200_OK)


class SalidaDisponibleViewSet(viewsets.ModelViewSet):
    """Gestión de salidas (profesor/admin) y listado para alumnos"""
    queryset = SalidaDisponible.objects.select_related('profesor', 'zona').all()
    serializer_class = SalidaDisponibleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser() | permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(fecha__gte=timezone.now().date())
        if user.is_staff:
            return qs
        if hasattr(user, 'profesor'):
            return qs.filter(profesor=user.profesor)
        # Alumnos: filtrar por zona de su última solicitud
        ult_solicitud = Solicitud.objects.filter(telefono=user.username).order_by('-fecha_inscripcion').first()
        if ult_solicitud:
            return qs.filter(zona=ult_solicitud.zona)
        return qs.none()


class ReservaViewSet(viewsets.ModelViewSet):
    """Crear reservas, confirmar y rechazar"""
    queryset = Reserva.objects.select_related('alumno', 'salida').all()
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        if hasattr(user, 'profesor'):
            # Profesor ve reservas para sus salidas
            return super().get_queryset().filter(salida__profesor=user.profesor)
        # Alumno ve sus reservas
        return super().get_queryset().filter(alumno=user)

    def perform_create(self, serializer):
        serializer.save(alumno=self.request.user)

    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        reserva = self.get_object()
        reserva.estado = 'C'
        reserva.updated_at = timezone.now()
        reserva.save()
        return Response(self.get_serializer(reserva).data)

    @action(detail=True, methods=['post'])
    def rechazar(self, request, pk=None):
        reserva = self.get_object()
        reserva.estado = 'R'
        reserva.updated_at = timezone.now()
        reserva.save()
        return Response(self.get_serializer(reserva).data)

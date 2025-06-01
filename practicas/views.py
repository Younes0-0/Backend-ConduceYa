# practicas/views.py
from django.utils import timezone
from rest_framework import viewsets, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Zona, Solicitud, SalidaDisponible, Reserva
from .serializers import (
    ZonaSerializer,
    SolicitudSerializer,
    SalidaDisponibleSerializer,
    ReservaSerializer,
)
from citas.permissions import EsProfesor, EsProfesorDueño  # asegúrate de tenerlos
# ---------------------------------------------------------------------------


# ════════════════════════════════  ZONAS  ════════════════════════════════ #
class ZonaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de zonas de examen.
    Solo el personal administrativo o 'staff' puede gestionarlas.
    """
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    permission_classes = [permissions.IsAdminUser]


# ═══════════════════════════════  SOLICITUDES  ═══════════════════════════ #
class SolicitudViewSet(viewsets.ModelViewSet):
    """
    Gestión de solicitudes de plaza para una zona y fecha concreta.
    Cualquier usuario autenticado puede crear; listar o modificar
    requiere rol de administrador.
    """
    queryset = Solicitud.objects.all().order_by("fecha_inscripcion")
    serializer_class = SolicitudSerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve", "update",
                           "partial_update", "destroy"}:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAdminUser],
        url_path="invitar",
    )
    def invitar(self, request, pk=None):
        """
        Marca la solicitud como INVITADA y,
        opcionalmente, crea una reserva pendiente.
        """
        solicitud: Solicitud = self.get_object()
        solicitud.estado = Solicitud.Estados.INVITADA
        solicitud.save(update_fields=["estado", "updated_at"])

        # ↪️  Hook: aquí podrías generar automáticamente una Reserva pendiente
        #          asociada a la salida disponible que definas en tu dominio.
        return Response({"status": "invitada"}, status=status.HTTP_200_OK)


# ═══════════════════════════════  SALIDAS  ═══════════════════════════════ #
class SalidaDisponibleViewSet(viewsets.ModelViewSet):
    """
    Gestión de 'salidas' o turnos de examen práctico.
    - Profesores: pueden crear/editar las de su agenda.
    - Staff: gestión completa.
    - Alumnos: solo listan las que correspondan a su zona.
    """
    queryset = (SalidaDisponible.objects
                .select_related("profesor", "zona"))
    serializer_class = SalidaDisponibleSerializer

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [permissions.IsAdminUser | EsProfesor]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset().filter(fecha__gte=timezone.now().date())
        user = self.request.user

        if user.is_staff:
            return qs
        if hasattr(user, "profesor"):
            return qs.filter(profesor=user.profesor)

        # Alumno → filtra por zona de su última solicitud
        ult_solicitud = (Solicitud.objects
                         .filter(alumno=user)
                         .order_by("-fecha_inscripcion")
                         .first())
        return qs.filter(zona=ult_solicitud.zona) if ult_solicitud else qs.none()


# ═══════════════════════════════  RESERVAS  ══════════════════════════════ #
class ReservaViewSet(viewsets.ModelViewSet):
    """
    Reserva de un alumno para una 'SalidaDisponible'.
    Acciones extra:
      • POST /reservas/{id}/confirmar/
      • POST /reservas/{id}/rechazar/
    """
    queryset = (Reserva.objects
                .select_related("alumno", "salida", "salida__profesor"))
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    # ---------- Queryset filtrado por rol -------------------------------- #
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        if hasattr(user, "profesor"):
            return super().get_queryset().filter(salida__profesor=user.profesor)
        return super().get_queryset().filter(alumno=user)

    # ---------- Crear ----------------------------------------------------- #
    def perform_create(self, serializer):
        salida = serializer.validated_data["salida"]

        # 1) No reservar si ya hay una reserva para esa salida
        if Reserva.objects.filter(salida=salida).exists():
            raise serializers.ValidationError(
                "Esta salida ya tiene una reserva asociada."
            )

        # 2) Evita que el profesor reserve su propia salida
        if (hasattr(self.request.user, "profesor")
                and salida.profesor == self.request.user.profesor):
            raise serializers.ValidationError(
                "No puedes reservar tu propia salida."
            )

        serializer.save(
            alumno=self.request.user,
            estado=Reserva.Estados.PENDIENTE,
        )

    # ---------- Confirmar ------------------------------------------------- #
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAdminUser | EsProfesorDueño],
    )
    def confirmar(self, request, pk=None):
        reserva: Reserva = self.get_object()

        if reserva.estado != Reserva.Estados.PENDIENTE:
            return Response(
                {"error": "La reserva ya fue gestionada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reserva.estado = Reserva.Estados.CONFIRMADA
        reserva.save(update_fields=["estado", "updated_at"])
        return Response(self.get_serializer(reserva).data)

    # ---------- Rechazar -------------------------------------------------- #
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAdminUser | EsProfesorDueño],
    )
    def rechazar(self, request, pk=None):
        reserva: Reserva = self.get_object()

        if reserva.estado != Reserva.Estados.PENDIENTE:
            return Response(
                {"error": "La reserva ya fue gestionada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reserva.estado = Reserva.Estados.RECHAZADA
        reserva.save(update_fields=["estado", "updated_at"])
        return Response(self.get_serializer(reserva).data)

# citas/views.py
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Profesor, HorarioDisponible, ClasePractica
from .serializers import (
    ProfesorSerializer,
    HorarioDisponibleSerializer,
    ClasePracticaSerializer,
)
from .permissions import EsAdmin, EsProfesor, EsProfesorDueño   # ya definidos

User = get_user_model()

# ═════════════════════════════  PROFESORES  ═════════════════════════════ #


class ProfesorViewSet(viewsets.ModelViewSet):
    """CRUD de profesores – solo administradores."""
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    permission_classes = [EsAdmin]


# ═══════════════════════════  HORARIOS DISPONIBLES  ═════════════════════ #
class HorarioDisponibleViewSet(viewsets.ModelViewSet):
    """
    - Profesores: CRUD de sus propios horarios.
    - Admins: CRUD global.
    - Alumnos: sólo lectura de huecos libres.
    """
    queryset = HorarioDisponible.objects.select_related("profesor__usuario")
    serializer_class = HorarioDisponibleSerializer

    # ----- permisos dinámicos ------------------------------------------- #
    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [EsProfesor | IsAdminUser]
        return [IsAuthenticated()]

    # ----- filtro por rol ------------------------------------------------ #
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return qs
        if hasattr(user, "profesor"):
            return qs.filter(profesor=user.profesor)
        # Alumno → sólo huecos no reservados
        return qs.exclude(id__in=ClasePractica.objects.values_list("horario", flat=True))

    # ----- asignar profesor automático ---------------------------------- #
    def perform_create(self, serializer):
        if hasattr(self.request.user, "profesor"):
            serializer.save(profesor=self.request.user.profesor)
        else:
            raise serializers.ValidationError(
                "Sólo los profesores crean horarios.")


# ═════════════════════════════  CLASES PRÁCTICAS  ═══════════════════════ #
class ClasePracticaViewSet(viewsets.ModelViewSet):
    """
    Reservas de clase práctica.
    Endpoints extra:
      • GET  /clases-practicas/mias/
      • POST /clases-practicas/agendar/
      • DELETE /clases-practicas/{id}/cancelar/
    """
    queryset = ClasePractica.objects.select_related(
        "alumno", "horario__profesor")
    serializer_class = ClasePracticaSerializer
    permission_classes = [IsAuthenticated & (EsProfesorDueño | IsAdminUser)]

    # -------- queryset por rol ------------------------------------------ #
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        if hasattr(user, "profesor"):
            return super().get_queryset().filter(horario__profesor=user.profesor)
        return super().get_queryset().filter(alumno=user)

    # -------- bloquear CRUD directo p/ alumnos y profes ----------------- #
    def create(self, *a, **kw):
        return Response({"detail": "Usa /agendar/"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, *a, **kw):
        return Response({"detail": "No permitido"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
    partial_update = update

    def destroy(self, *a, **kw):
        return Response({"detail": "Usa /cancelar/"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # -------- LISTAR MIS CITAS ----------------------------------------- #
    @action(detail=False, methods=["get"])
    def mias(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    # -------- AGENDAR --------------------------------------------------- #
    @action(detail=False, methods=["post"], url_path="agendar")
    def agendar(self, request):
        horario_id = request.data.get("horario_id")
        if not horario_id:
            return Response({"error": "Se requiere horario_id"}, status=400)

        horario = get_object_or_404(HorarioDisponible, id=horario_id)

        if ClasePractica.objects.filter(horario=horario).exists():
            return Response({"error": "Horario ya reservado"}, status=400)

        if hasattr(request.user, "profesor") and horario.profesor == request.user.profesor:
            return Response({"error": "No puedes agendar tu propio horario"}, status=400)

        clase = ClasePractica.objects.create(
            alumno=request.user, horario=horario)
        return Response(self.get_serializer(clase).data, status=201)

    # -------- CANCELAR -------------------------------------------------- #
    @action(detail=True, methods=["delete"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        clase = self.get_object()
        clase.delete()
        return Response(status=204)

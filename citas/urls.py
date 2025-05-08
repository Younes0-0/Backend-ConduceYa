from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfesorViewSet,
    HorarioDisponibleViewSet,
    ClasePracticaViewSet,
    current_user,
    agendar_cita,
    ver_citas,
    cancelar_cita,
    listar_usuarios,
    ver_disponibilidad,
)

router = DefaultRouter()
router.register(r'profesores', ProfesorViewSet, basename='profesor')
router.register(r'horarios', HorarioDisponibleViewSet, basename='horario')
router.register(r'clases', ClasePracticaViewSet, basename='clase')

urlpatterns = [
    # Rutas automáticas CRUD
    path('', include(router.urls)),

    # Usuario actual
    path('user/', current_user, name='current_user'),

    # Gestión de citas
    path('citas/agendar/', agendar_cita, name='citas-agendar'),
    path('citas/', ver_citas, name='citas-ver'),
    path('citas/cancelar/<int:cita_id>/', cancelar_cita, name='citas-cancelar'),

    # Usuarios (solo admin)
    path('usuarios/', listar_usuarios, name='listar-usuarios'),

    # Disponibilidad de horarios
    path('disponibilidad/', ver_disponibilidad, name='ver_disponibilidad'),
]

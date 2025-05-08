# Vamos a definir las rutas de la API para que el frontend pueda hacer solicitudes.
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ProfesorViewSet,
    HorarioDisponibleViewSet,
    ClasePracticaViewSet,
    current_user,
    # Asegúrate de que estos estén importados si los necesitas:
    agendar_cita,
    ver_citas,
    cancelar_cita,
    listar_usuarios,
    ver_disponibilidad,
)

router = DefaultRouter()
router.register(r'profesores', ProfesorViewSet)
router.register(r'horarios', HorarioDisponibleViewSet)
router.register(r'clases', ClasePracticaViewSet)

urlpatterns = [
    # Endpoints automáticos
    path('', include(router.urls)),

    # Endpoint para obtener el usuario actual (usado por Astro frontend)
    path('user/', current_user, name='current_user'),

    # Endpoints personalizados para citas
    path('citas/agendar/', agendar_cita, name='citas-agendar'),
    path('citas/', ver_citas, name='citas-ver'),
    path('citas/cancelar/<int:cita_id>/', cancelar_cita, name='citas-cancelar'),

    # Endpoint para ver todos los usuarios (solo admin)
    path('usuarios/', listar_usuarios, name='listar-usuarios'),

    # JWT Auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Información del usuario autenticado (redundante si usas current_user)
    #path('auth/user/', obtener_usuario, name='obtener_usuario'),

    # Ver horarios disponibles
    path('disponibilidad/', ver_disponibilidad, name='ver_disponibilidad'),
]


 
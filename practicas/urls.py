from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ZonaViewSet,
    SolicitudViewSet,
    SalidaDisponibleViewSet,
    ReservaViewSet,
)

router = DefaultRouter()
router.register(r'zonas', ZonaViewSet, basename='zona')
router.register(r'solicitudes', SolicitudViewSet, basename='solicitud')
router.register(r'salidas', SalidaDisponibleViewSet, basename='salida')
router.register(r'reservas', ReservaViewSet, basename='reserva')

urlpatterns = [
    # Rutas automáticas para la app practicas
    path('practicas', include(router.urls)),
]
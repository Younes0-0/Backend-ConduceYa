# practicas/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    ZonaViewSet,
    SolicitudViewSet,
    SalidaDisponibleViewSet,
    ReservaViewSet,
)

router = DefaultRouter()
router.register("zonas",        ZonaViewSet,        basename="zonas")
router.register("solicitudes",  SolicitudViewSet,   basename="solicitudes")
router.register("salidas",      SalidaDisponibleViewSet, basename="salidas")
router.register("reservas",     ReservaViewSet,     basename="reservas")

urlpatterns = router.urls     # 👈 sin path extra

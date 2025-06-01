from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProfesorViewSet, HorarioDisponibleViewSet, ClasePracticaViewSet

router = DefaultRouter()
router.register(
    "profesores-agenda",      # evita choque
    ProfesorViewSet,
    basename="profesores-agenda"
)
router.register('horarios-disponibles', HorarioDisponibleViewSet,
                basename='horarios-disponibles')
router.register('clases-practicas', ClasePracticaViewSet,
                basename='clases-practicas')

# ¡Solo el router!
urlpatterns = router.urls

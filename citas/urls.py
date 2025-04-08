# Vamos a definir las rutas de la API para que el frontend pueda hacer solicitudes.
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfesorViewSet, HorarioDisponibleViewSet, ClasePracticaViewSet, current_user

router = DefaultRouter()
router.register(r'profesores', ProfesorViewSet)
router.register(r'horarios', HorarioDisponibleViewSet)
router.register(r'clases', ClasePracticaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', current_user),  # 👈 Esta línea conecta el endpoint que pide Astro
]


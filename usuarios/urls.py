from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfesorViewSet, AlumnoViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profesores', ProfesorViewSet, basename='profesor')
router.register(r'alumnos', AlumnoViewSet, basename='alumno')

urlpatterns = [
    path('', include(router.urls)),
]
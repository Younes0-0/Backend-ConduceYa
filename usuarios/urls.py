from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfesorViewSet, AlumnoViewSet

router = DefaultRouter()
# 👇  Usa basenames plural-kebab y anotaciones coherentes
router.register("users",       UserViewSet,      basename="users")
router.register("profesores",  ProfesorViewSet,  basename="profesores")
router.register("alumnos",     AlumnoViewSet,    basename="alumnos")

# 👉  Sin “/” inicial en path y sin lista extra: exportamos el router tal cual
urlpatterns = router.urls

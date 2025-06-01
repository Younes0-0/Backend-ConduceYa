# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# 👉 importamos los routers de cada app
from citas.urls import router as citas_router
from practicas.urls import router as practicas_router
from usuarios.urls import router as usuarios_router

# 🔗 Router maestro (versión 1)
api_router = DefaultRouter()
api_router.registry.extend(citas_router.registry)
api_router.registry.extend(practicas_router.registry)
api_router.registry.extend(usuarios_router.registry)

urlpatterns = [
    # Django-admin
    path('admin/', admin.site.urls),

    # API unificada
    path('api/v1/', include(api_router.urls)),

    # JWT dentro de la misma versión
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

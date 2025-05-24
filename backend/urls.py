from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 🔥 Rutas de la administración de Django
    path('admin/', admin.site.urls),
    # 🔥 Rutas de la API
    path('api/citas', include('citas.urls')),
    path('api/practicas', include('practicas.urls')),
    path('api/usuarios', include('usuarios.urls')),
    # 🔥 Rutas para obtener y refrescar tokens JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🔥 Rutas de la API de practicas
]

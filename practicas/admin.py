from django.contrib import admin
from .models import Zona, Solicitud, SalidaDisponible, Reserva

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'zona', 'sesion_preferida', 'estado', 'fecha_inscripcion')
    list_filter = ('zona', 'sesion_preferida', 'estado')
    search_fields = ('nombre', 'telefono')
    ordering = ('-fecha_inscripcion',)

@admin.register(SalidaDisponible)
class SalidaDisponibleAdmin(admin.ModelAdmin):
    list_display = ('id', 'profesor', 'zona', 'fecha', 'sesion', 'cupo_maximo')
    list_filter = ('zona', 'sesion')
    date_hierarchy = 'fecha'

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'salida', 'estado', 'created_at', 'updated_at')
    list_filter = ('estado', 'salida__fecha', 'salida__sesion')
    search_fields = ('alumno__username',)
    ordering = ('-created_at',)


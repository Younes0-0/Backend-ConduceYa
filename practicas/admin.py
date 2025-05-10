from django.contrib import admin
from .models import (
    Zona,
    Permiso,
    Fase,
    PermisoFase,
    Solicitud,
    ExamenIntento,
    SalidaDisponible,
    Reserva,
)

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(Fase)
class FaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'orden')
    list_editable = ('orden',)
    ordering = ('orden',)

@admin.register(PermisoFase)
class PermisoFaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'permiso', 'fase', 'orden')
    list_filter = ('permiso', 'fase')
    ordering = ('permiso', 'orden')

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'nombre', 'telefono', 'zona', 'permiso', 'sesion_preferida',
        'fecha_teorico', 'fecha_inscripcion', 'estado', 'fase_actual'
    )
    list_filter = ('zona', 'permiso', 'sesion_preferida', 'estado')
    search_fields = ('nombre', 'telefono')
    readonly_fields = ('fecha_inscripcion',)
    fieldsets = (
        (None, {
            'fields': (
                ('nombre', 'telefono'),
                'zona', 'permiso', 'sesion_preferida',
                'fecha_teorico', 'notas',
            )
        }),
        ('Estado y Avance', {
            'fields': ('estado', 'fase_actual'),
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('fecha_inscripcion',),
        }),
    )

@admin.register(ExamenIntento)
class ExamenIntentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitud', 'fase', 'fecha_intento', 'aprobado')
    list_filter = ('fase', 'aprobado')
    search_fields = ('solicitud__nombre',)

@admin.register(SalidaDisponible)
class SalidaDisponibleAdmin(admin.ModelAdmin):
    list_display = ('id', 'profesor', 'zona', 'fecha', 'sesion', 'cupo_maximo')
    list_filter = ('zona', 'sesion')
    date_hierarchy = 'fecha'

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'salida', 'estado', 'created_at')
    list_filter = ('estado', 'salida__fecha', 'salida__sesion')
    search_fields = ('alumno__username',)

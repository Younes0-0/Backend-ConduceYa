from django.contrib import admin
from .models import (
    Zona, Permiso, Fase, PermisoFase,
    Solicitud, ExamenIntento, SalidaDisponible, Reserva
)


class PermisoFaseInline(admin.TabularInline):
    model = PermisoFase
    extra = 1
    verbose_name = 'Fase asignada'
    verbose_name_plural = 'Fases asignadas'


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')
    inlines = [PermisoFaseInline]


@admin.register(Fase)
class FaseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden')
    list_editable = ('orden',)
    ordering = ('orden',)


@admin.register(PermisoFase)
class PermisoFaseAdmin(admin.ModelAdmin):
    list_display = ('permiso', 'fase', 'orden')
    list_filter = ('permiso',)


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = (
        'alumno', 'zona', 'permiso', 'sesion_preferida', 'estado', 'fecha_inscripcion'
    )
    list_filter = ('zona', 'permiso', 'estado', 'sesion_preferida')
    search_fields = (
        'alumno__username', 'alumno__first_name', 'alumno__last_name', 'alumno__email'
    )
    readonly_fields = ('fecha_inscripcion',)
    fieldsets = (
        (None, {
            'fields': ('alumno', 'zona', 'permiso', 'sesion_preferida', 'notas')
        }),
        ('Estado y Fase', {
            'fields': ('estado', 'fase_actual')
        }),
        ('Fechas', {
            'fields': ('fecha_teorico', 'fecha_inscripcion')
        }),
    )


@admin.register(ExamenIntento)
class ExamenIntentoAdmin(admin.ModelAdmin):
    list_display = ('solicitud', 'fase', 'fecha_intento', 'aprobado')
    list_filter = ('fase', 'aprobado')
    date_hierarchy = 'fecha_intento'


@admin.register(SalidaDisponible)
class SalidaDisponibleAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'zona', 'sesion', 'fecha', 'cupo_maximo')
    list_filter = ('zona', 'sesion', 'profesor')
    date_hierarchy = 'fecha'
    search_fields = ('profesor__usuario__username',)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'salida', 'estado', 'created_at')
    list_filter = ('estado',)
    search_fields = ('alumno__username',)
    readonly_fields = ('created_at', 'updated_at')

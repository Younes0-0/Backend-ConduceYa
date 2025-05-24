from django.contrib import admin
from .models import HorarioDisponible, ClasePractica


@admin.register(HorarioDisponible)
class HorarioDisponibleAdmin(admin.ModelAdmin):
    list_display = ('id', 'profesor', 'fecha_hora_inicio')


@admin.register(ClasePractica)
class ClasePracticaAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'horario')

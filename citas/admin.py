from django.contrib import admin
from .models import Profesor, HorarioDisponible, ClasePractica

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'nombre_usuario')

    def nombre_usuario(self, obj):
        return obj.usuario.username

@admin.register(HorarioDisponible)
class HorarioDisponibleAdmin(admin.ModelAdmin):
    list_display = ('id', 'profesor', 'fecha_hora_inicio')

@admin.register(ClasePractica)
class ClasePracticaAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'horario')

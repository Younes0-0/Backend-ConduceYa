from django.contrib import admin
from .models import Profesor, HorarioDisponible, ClasePractica

admin.site.register(Profesor)
admin.site.register(HorarioDisponible)
admin.site.register(ClasePractica)

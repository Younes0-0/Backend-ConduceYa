from django.db import models
from django.contrib.auth.models import User

class Profesor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username

class HorarioDisponible(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="horarios")
    fecha_hora_inicio = models.DateTimeField(unique=True)

    def __str__(self):
        return f"{self.profesor.usuario.username} - {self.fecha_hora_inicio}"

class ClasePractica(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clases")
    horario = models.OneToOneField(HorarioDisponible, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.alumno.username} - {self.horario.fecha_hora_inicio}"

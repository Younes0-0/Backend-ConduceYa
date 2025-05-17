from django.db import models
from django.conf import settings
from usuarios.models import Profesor


class HorarioDisponible(models.Model):
    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.CASCADE,
        related_name="horarios"
    )
    fecha_hora_inicio = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['profesor', 'fecha_hora_inicio'],
                name='unique_horario_por_profesor'
            )
        ]


class ClasePractica(models.Model):
    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clases"
    )
    horario = models.OneToOneField(
        HorarioDisponible,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.alumno.username} - {self.horario.fecha_hora_inicio}"

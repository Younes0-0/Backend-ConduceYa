from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from citas.models import Profesor


class Zona(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'

    def __str__(self):
        return self.nombre


class Solicitud(models.Model):
    SESION_CHOICES = [
        ('M', 'Mañana'),
        ('T', 'Tarde'),
        ('B', 'Mixta'),
    ]
    ESTADO_CHOICES = [
        ('S', 'Solicitado'),
        ('I', 'Invitado'),
        ('C', 'Confirmado'),
        ('R', 'Rechazado'),
        ('E', 'Espera'),
        ('A', 'Asistido'),
        ('N', 'No Asistido'),
    ]

    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    zona = models.ForeignKey(Zona, on_delete=models.PROTECT, related_name='solicitudes')
    sesion_preferida = models.CharField(max_length=1, choices=SESION_CHOICES)
    fecha_teorico = models.DateField(null=True, blank=True)
    fecha_inscripcion = models.DateTimeField(default=timezone.now)
    notas = models.TextField(blank=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='S')

    class Meta:
        ordering = ['fecha_inscripcion']
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

    def __str__(self):
        return f"{self.nombre} ({self.get_sesion_preferida_display()} - {self.zona})"


class SalidaDisponible(models.Model):
    SESION_CHOICES = Solicitud.SESION_CHOICES

    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.CASCADE,
        related_name='salidas'
    )
    zona = models.ForeignKey(Zona, on_delete=models.PROTECT, related_name='salidas')
    fecha = models.DateField()
    sesion = models.CharField(max_length=1, choices=SESION_CHOICES)
    cupo_maximo = models.PositiveSmallIntegerField(default=3)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profesor', 'fecha', 'sesion'], name='unique_salida_profesor')
        ]
        verbose_name = 'Salida Disponible'
        verbose_name_plural = 'Salidas Disponibles'

    def __str__(self):
        return f"{self.profesor.usuario.username} - {self.get_sesion_display()} {self.fecha}"


class Reserva(models.Model):
    ESTADO_CHOICES = Solicitud.ESTADO_CHOICES

    alumno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    salida = models.ForeignKey(
        SalidaDisponible,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='S')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('alumno', 'salida')]
        ordering = ['created_at']
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"Reserva de {self.alumno.username} para {self.salida} ({self.get_estado_display()})"

from django.db import models
from django.utils import timezone
from django.conf import settings
from usuarios.models import Profesor, Alumno


class Zona(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'

    def __str__(self):
        return self.nombre


class Permiso(models.Model):
    """Tipos de permiso de conducir disponibles"""
    codigo = models.CharField(max_length=2, unique=True)
    descripcion = models.CharField(max_length=50)
    fases = models.ManyToManyField(
        'Fase', through='PermisoFase', related_name='permisos'
    )

    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class Fase(models.Model):
    """Etapas de examen: Teórico, Destreza, Circulación"""
    nombre = models.CharField(max_length=20, unique=True)
    orden = models.PositiveSmallIntegerField(
        help_text="Orden de la fase dentro del permiso")

    class Meta:
        ordering = ['orden']
        verbose_name = 'Fase'
        verbose_name_plural = 'Fases'

    def __str__(self):
        return self.nombre


class PermisoFase(models.Model):
    """Relación ordenada entre Permiso y Fase"""
    permiso = models.ForeignKey(
        Permiso,
        on_delete=models.CASCADE,
        related_name='permisofases',
        related_query_name='permisofase'
    )
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    orden = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [('permiso', 'fase')]
        ordering = ['orden']
        verbose_name = 'Permiso - Fase'
        verbose_name_plural = 'Permisos - Fases'

    def __str__(self):
        return f"{self.permiso.codigo}: {self.fase.nombre}"


class Solicitud(models.Model):
    """
    Solicitud asociada a un alumno registrado.
    """
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

    alumno = models.ForeignKey(
        Alumno,
        on_delete=models.CASCADE,
        related_name='solicitudes',
        default=1,
    )
    zona = models.ForeignKey(
        Zona, on_delete=models.PROTECT, related_name='solicitudes')
    permiso = models.ForeignKey(
        Permiso,
        on_delete=models.PROTECT,
        related_name='solicitudes',
        related_query_name='solicitud'
    )
    sesion_preferida = models.CharField(max_length=1, choices=SESION_CHOICES)
    fecha_teorico = models.DateField(null=True, blank=True)
    fecha_inscripcion = models.DateTimeField(default=timezone.now)
    notas = models.TextField(blank=True)
    estado = models.CharField(
        max_length=1, choices=ESTADO_CHOICES, default='S')
    fase_actual = models.ForeignKey(
        Fase,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='solicitudes'
    )

    class Meta:
        ordering = ['fecha_inscripcion']
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

    def __str__(self):
        nombre = self.alumno.usuario.get_full_name() or self.alumno.usuario.username
        return f"{nombre} - {self.get_sesion_preferida_display()} ({self.zona})"

    def fases_permitidas(self):
        return [pf.fase for pf in self.permiso.permisofases.all()]

    def puede_avanzar(self, nueva_fase):
        fases = self.fases_permitidas()
        if self.fase_actual not in fases:
            return nueva_fase == fases[0]
        idx = fases.index(self.fase_actual)
        return idx + 1 < len(fases) and nueva_fase == fases[idx + 1]


class ExamenIntento(models.Model):
    """Registro de cada intento de examen por fase"""
    solicitud = models.ForeignKey(
        Solicitud, on_delete=models.CASCADE, related_name='intentos')
    fase = models.ForeignKey(Fase, on_delete=models.PROTECT)
    fecha_intento = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField()

    class Meta:
        ordering = ['-fecha_intento']
        verbose_name = 'Intento de Examen'
        verbose_name_plural = 'Intentos de Examen'

    def __str__(self):
        estado = 'Aprobado' if self.aprobado else 'Rechazado'
        return f"{self.solicitud.alumno.username} - {self.fase.nombre} ({estado})"


class SalidaDisponible(models.Model):
    SESION_CHOICES = Solicitud.SESION_CHOICES

    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.CASCADE,
        related_name='salidas'
    )
    zona = models.ForeignKey(
        Zona, on_delete=models.PROTECT, related_name='salidas')
    fecha = models.DateField()
    sesion = models.CharField(max_length=1, choices=SESION_CHOICES)
    cupo_maximo = models.PositiveSmallIntegerField(default=3)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['profesor', 'fecha', 'sesion'], name='unique_salida_profesor')
        ]
        verbose_name = 'Salida Disponible'
        verbose_name_plural = 'Salidas Disponibles'

    def __str__(self):
        return f"{self.profesor.usuario.username} - {self.get_sesion_display()} {self.fecha}"


class Reserva(models.Model):
    ESTADO_CHOICES = Solicitud.ESTADO_CHOICES

    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    salida = models.ForeignKey(
        SalidaDisponible,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    estado = models.CharField(
        max_length=1, choices=ESTADO_CHOICES, default='S')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('alumno', 'salida')]
        ordering = ['created_at']
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"Reserva de {self.alumno.username} para {self.salida} ({self.get_estado_display()})"

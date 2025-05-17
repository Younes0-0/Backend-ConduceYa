from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Usuario personalizado con nombre, apellidos y rol.
    """
    class Roles(models.TextChoices):
        ALUMNO = 'A', _('Alumno')
        PROFESOR = 'P', _('Profesor')
        ADMINISTRADOR = 'AD', _('Administrador')

    first_name = models.CharField(_('Nombre'), max_length=30)
    last_name = models.CharField(_('Apellidos'), max_length=30)
    rol = models.CharField(
        _('Rol'),
        max_length=2,
        choices=Roles.choices,
        default=Roles.ALUMNO
    )

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_alumno(self):
        """Indica si el usuario es alumno."""
        return self.rol == self.Roles.ALUMNO

    @property
    def is_profesor(self):
        """Indica si el usuario es profesor."""
        return self.rol == self.Roles.PROFESOR

    @property
    def is_administrador(self):
        """Indica si el usuario es administrador del sistema."""
        return self.rol == self.Roles.ADMINISTRADOR


class Profesor(models.Model):
    """
    Perfil adicional para profesores, con permisos personalizados.
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_profesor'
    )
    permisos = models.JSONField(
        _('Permisos'),
        default=dict,
        help_text=_('Permisos específicos para el profesor')
    )

    class Meta:
        verbose_name = _('profesor')
        verbose_name_plural = _('profesores')

    def __str__(self):
        return str(self.usuario)


class Alumno(models.Model):
    """
    Perfil adicional para alumnos.
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_alumno'
    )

    class Meta:
        verbose_name = _('alumno')
        verbose_name_plural = _('alumnos')

    def __str__(self):
        return str(self.usuario)

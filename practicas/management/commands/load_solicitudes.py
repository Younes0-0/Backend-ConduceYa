from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from practicas.models import Solicitud

class Command(BaseCommand):
    help = 'Crea usuarios Django a partir de las solicitudes existentes'

    def handle(self, *args, **options):
        solicitudes = Solicitud.objects.all()
        for sol in solicitudes:
            telefono = sol.telefono.strip()
            if not telefono:
                self.stdout.write(self.style.ERROR(f"Solicitud {sol.id} sin teléfono, no se crea usuario"))
                continue

            username = telefono  # usar teléfono como username
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'El usuario {username} ya existe'))
                continue

            # Dividir nombre en first_name y last_name
            parts = sol.nombre.strip().split()
            first_name = parts[0]
            last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

            # Crear usuario con contraseña igual al teléfono
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=telefono
            )
            self.stdout.write(self.style.SUCCESS(f'Usuario creado: {username}'))

            # Si el modelo Solicitud tiene campo user, vincularlo
            if hasattr(sol, 'user'):
                sol.user = user
                sol.save()
                self.stdout.write(self.style.SUCCESS(f'Usuario vinculado a solicitud {sol.id}'))

        self.stdout.write(self.style.SUCCESS('Proceso de creación de usuarios completado.'))

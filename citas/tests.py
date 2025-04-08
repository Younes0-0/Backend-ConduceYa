from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Profesor, HorarioDisponible, ClasePractica
from django.utils import timezone
from datetime import timedelta

class CitaTests(TestCase):
    def setUp(self):
        # Crear usuario profesor
        self.user_profesor = User.objects.create_user(username='profe', password='1234')
        self.profesor = Profesor.objects.create(usuario=self.user_profesor)

        # Crear usuario alumno
        self.user_alumno = User.objects.create_user(username='alumno', password='1234')

        # Cliente autenticado como profesor
        self.client_profe = APIClient()
        self.client_profe.force_authenticate(user=self.user_profesor)

        # Cliente autenticado como alumno
        self.client_alumno = APIClient()
        self.client_alumno.force_authenticate(user=self.user_alumno)

    def test_profesor_puede_crear_horario(self):
        fecha = timezone.now() + timedelta(days=1)
        response = self.client_profe.post('/api/horarios/', {'fecha_hora_inicio': fecha.isoformat()})
        self.assertEqual(response.status_code, 201)

    def test_alumno_no_puede_crear_horario(self):
        fecha = timezone.now() + timedelta(days=1)
        response = self.client_alumno.post('/api/horarios/', {'fecha_hora_inicio': fecha.isoformat()})
        self.assertEqual(response.status_code, 400)

    def test_alumno_puede_reservar_clase(self):
        # Profe crea horario
        fecha = timezone.now() + timedelta(days=2)
        horario = HorarioDisponible.objects.create(profesor=self.profesor, fecha_hora_inicio=fecha)

        # Alumno reserva ese horario
        response = self.client_alumno.post('/api/clases/', {'horario': horario.id, 'alumno': self.user_alumno.id})
        self.assertEqual(response.status_code, 201)

    def test_alumno_no_puede_reservar_horario_ocupado(self):
        fecha = timezone.now() + timedelta(days=3)
        horario = HorarioDisponible.objects.create(profesor=self.profesor, fecha_hora_inicio=fecha)
        ClasePractica.objects.create(alumno=self.user_alumno, horario=horario)

        # Otro alumno intenta reservar el mismo horario
        otro_alumno = User.objects.create_user(username='otro', password='1234')
        client_otro = APIClient()
        client_otro.force_authenticate(user=otro_alumno)
        response = client_otro.post('/api/clases/', {'horario': horario.id, 'alumno': otro_alumno.id})

        self.assertEqual(response.status_code, 400)  # Debería fallar


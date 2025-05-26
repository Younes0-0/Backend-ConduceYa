from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from practicas.models import Solicitud, Zona, Permiso
from usuarios.models import Alumno

User = get_user_model()


class Command(BaseCommand):
    help = 'Importa alumnos y solicitudes desde una lista interna'

    ALUMNOS = [
        {'nombre': 'NAZHA FADLI', 'telefono': '617075961', 'sesion': 'm',
            'fecha_teorico': '17/01/24', 'zona': 'Ejido', 'notas': 'ELLA AVISA'},
        {'nombre': 'ALICIA RODRIGUEZ', 'telefono': '635737320', 'sesion': 'm',
            'fecha_teorico': '03/09/24', 'zona': 'Motril', 'notas': 'ELLA AVISA'},
        {'nombre': 'HASNA BAKOUH ALIT', 'telefono': '612582649', 'sesion': 'm/t',
            'fecha_teorico': '09/05/24', 'zona': 'El ejido', 'notas': '21/06/25'},
        {'nombre': 'YAMOU DIOP 6 pract', 'telefono': '602147133', 'sesion': 't',
            'fecha_teorico': '15/01/24', 'zona': 'Albuñol', 'notas': 'tiene que pagar'},
        {'nombre': 'YOUSSOUPH SAGNA', 'telefono': '631343392', 'sesion': 't',
            'fecha_teorico': '09/05/24', 'zona': 'El ejido', 'notas': 'tiene que pagar'},
        {'nombre': 'NAYARA CORTES GOMEZ', 'telefono': '664520001', 'sesion': 'm',
            'fecha_teorico': '25/04/24', 'zona': 'Matagorda', 'notas': 'tiene que pagar'},
        {'nombre': 'CONCEPCION SANTIAGO MUÑOZ', 'telefono': '610969976', 'sesion': 'm 9 mañana',
            'fecha_teorico': '25/04/24', 'zona': 'Matagorda', 'notas': '12/06/24 se pregunto el 08/01 ella avisa'},
        {'nombre': 'FRANCISCA AMADOR HEREDIA', 'telefono': '722439944', 'sesion': 'm/t',
            'fecha_teorico': '23/05/24', 'zona': 'Matagorda', 'notas': '25/06/24 no pago'},
        {'nombre': 'BABACAR THIOR', 'telefono': '642988232', 'sesion': 'm',
            'fecha_teorico': '15/10/24', 'zona': 'El ejido', 'notas': 'viki o pili'},
        {'nombre': 'MUSSA FATI', 'telefono': '632048647', 'sesion': 't JULIO',
            'fecha_teorico': '10/07/24', 'zona': 'El ejido', 'notas': ''},
        {'nombre': 'MARIA ISABEL CONDE', 'telefono': '695171917', 'sesion': 'm/t 23 JUNIO',
            'fecha_teorico': '20/08/24', 'zona': 'Albuñol', 'notas': '28/08/24'},
        {'nombre': 'CRISTIAN GARCIA RIVAS', 'telefono': '622174364', 'sesion': 'm',
            'fecha_teorico': '03/09/24', 'zona': 'Los castillas', 'notas': '16/09/24'},
        {'nombre': 'NAIRA RIVERA CORRAL', 'telefono': '642544491', 'sesion': 't',
            'fecha_teorico': '26/11/24', 'zona': 'El ejido', 'notas': '23/01/25 29-30 MAYO puede mañanas'},
        {'nombre': 'MARTA VARGAS MANZANO', 'telefono': '643867292', 'sesion': 'm/t 23 JUNIO',
            'fecha_teorico': '29/01/24', 'zona': 'Albuñol', 'notas': '29/01/25'},
        {'nombre': 'MIGUEL ANGEL DOÑA', 'telefono': '636667991', 'sesion': 'JUNIO/JULIO',
            'fecha_teorico': '23/01/25', 'zona': 'El ejido', 'notas': '03/02/25 el avisa'},
        {'nombre': 'MUSTAPHA BELHADJ', 'telefono': '603174571', 'sesion': '04/04/25', 'fecha_teorico': '2025',
            'zona': 'El ejido', 'notas': '03/02/25 a partir de las 16h?? no da señales'},
        {'nombre': 'BORJA MANRIQUE', 'telefono': '640188483', 'sesion': 't',
            'fecha_teorico': '07/03/25', 'zona': 'Albuñol', 'notas': '10/03/25'},
        {'nombre': 'HAISSOUNE ARAICH', 'telefono': '624651009', 'sesion': 'm',
            'fecha_teorico': '07/03/25', 'zona': 'El ejido', 'notas': '10/03/25 1º turno'},
        {'nombre': 'MOHAMED OUCHAIB', 'telefono': '617573382', 'sesion': 'TURNOS',
            'fecha_teorico': '26/11/24', 'zona': 'El ejido', 'notas': '17/03/25 05/05 puede pract tardes'},
        {'nombre': 'ABDENNAJI BAHAJOUB', 'telefono': '610994225', 'sesion': 't',
            'fecha_teorico': '24/03/25', 'zona': 'El ejido', 'notas': '25/03/25 a partir de las 16h'},
        {'nombre': 'MOHAMED ABDOUCHDAK', 'telefono': '631485414', 'sesion': 'm PRINC OCT',
            'fecha_teorico': '24/03/25', 'zona': 'El ejido', 'notas': '25/03/25'},
        {'nombre': 'FRANCISCO JOSE BERENGUER', 'telefono': '602815905', 'sesion': 'm JUNIO',
            'fecha_teorico': '12/12/24', 'zona': 'Albuñol', 'notas': '28/03/25'},
        {'nombre': 'SUKAYNA EL REGRAGUI', 'telefono': '643695343', 'sesion': 'm/t',
            'fecha_teorico': '23/01/25', 'zona': 'La mamola', 'notas': '02/04/25 profe mujer'},
        {'nombre': 'ABDELLAH BAHRAOUI GHANIMI', 'telefono': '602828754', 'sesion': 'm 1º TURNO JUNIO',
            'fecha_teorico': '29/10/24', 'zona': 'El ejido', 'notas': '03/04/25'},
        {'nombre': 'HICHAM ROUIFIK', 'telefono': '600433108', 'sesion': 'm/t',
            'fecha_teorico': '26/03/25', 'zona': 'El ejido', 'notas': '04/04/25'},
        {'nombre': 'MARI PAZ DE LA ROSA', 'telefono': '658259889', 'sesion': 'm',
            'fecha_teorico': '07/04/25', 'zona': 'Albuñol', 'notas': '08/04/25'},
        {'nombre': 'DANIEL LORENTE', 'telefono': '624656933', 'sesion': 'm/t', 'fecha_teorico': '07/04/25',
            'zona': 'Albuñol', 'notas': '09/04/25 22 JUNIO SE VA Y VUELVE 22 JULIO'},
        {'nombre': 'SAIDA OULED JILLALI', 'telefono': '612571419', 'sesion': 't',
            'fecha_teorico': '08/04/25', 'zona': 'Norias', 'notas': '04/04/25 recoger en cajamar'},
        {'nombre': 'RAMONA VICTORIA CLAPON', 'telefono': '666076834', 'sesion': 'm/t',
            'fecha_teorico': '07/04/25', 'zona': 'Matagorda', 'notas': '15/04/25 recoger en cajamar'},
        {'nombre': 'MOHAMED YASSINE BEDDOUKA', 'telefono': '613891837', 'sesion': 'm/t',
            'fecha_teorico': '17/09/24', 'zona': 'Matagorda', 'notas': '22/04/25 cajamar'},
        {'nombre': 'INMACULADA SABIO', 'telefono': '616776659', 'sesion': 't',
            'fecha_teorico': '22/04/25', 'zona': 'Melicena', 'notas': '23/04/25'},
        {'nombre': 'JUSTINO SUARES VAZ', 'telefono': '624380107', 'sesion': 'm',
            'fecha_teorico': '28/01/25', 'zona': 'Las norias', 'notas': '24/04/25 cajamar'},
        {'nombre': 'IRENE NAVARRO RODRIGUEZ', 'telefono': '622302703', 'sesion': 'm/t',
            'fecha_teorico': '07/04/25', 'zona': 'Almerimar', 'notas': '25/04/25'},
        {'nombre': 'RACHID SAMAD', 'telefono': '63137064', 'sesion': 't',
            'fecha_teorico': '28/04/25', 'zona': 'El ejido', 'notas': '05/05/25'},
        {'nombre': 'MOHAMED BELKBIR', 'telefono': '634093794', 'sesion': 'm/t',
            'fecha_teorico': '10/02/25', 'zona': 'Matagorda', 'notas': '06/05/25 recoger en megasa'},
        {'nombre': 'EVA MARIA MOLINA', 'telefono': '671129340', 'sesion': 'm/t',
            'fecha_teorico': '13/01/25', 'zona': 'Balanegra', 'notas': '07/05/25 recoger salida EN LA CABA'},
        {'nombre': 'NATALIA RUIZ', 'telefono': '677122537', 'sesion': 'm',
            'fecha_teorico': '24/03/25', 'zona': 'El ejido', 'notas': '08/05/25'},
        {'nombre': 'JUAN CARLOS VALENCIA', 'telefono': '631672713', 'sesion': 't',
            'fecha_teorico': '13/11/23', 'zona': 'El ejido', 'notas': '08/05/25'},
        {'nombre': 'AMINA NOUISSEL', 'telefono': '627024872', 'sesion': 'm', 'fecha_teorico': '08/05/25',
            'zona': 'Las norias', 'notas': '09/05/25 recoger en cajamar, a partir de las 8'},
        {'nombre': 'NAJWA NOUISSEL', 'telefono': '632006797', 'sesion': 'm', 'fecha_teorico': '08/05/25',
            'zona': 'Las norias', 'notas': '09/05/25 recoger en cajamar, a partir de las 8'},
        {'nombre': 'GEMMA TORNES', 'telefono': '613749829', 'sesion': 'm',
            'fecha_teorico': '11/03/24', 'zona': 'El ejido', 'notas': '09/05/25'}
    ]

    def handle(self, *args, **kwargs):
        permiso = Permiso.objects.first()
        if not permiso:
            self.stdout.write(self.style.ERROR(
                '❌ No hay permisos de conducir definidos.'))
            return

        for datos in self.ALUMNOS:
            nombre = datos['nombre'].strip()
            telefono = datos['telefono'].strip()
            sesion_raw = datos['sesion'].lower().strip()
            zona_nombre = datos['zona'].strip().capitalize()
            notas = datos.get('notas', '').strip()

            # Convertir sesión
            if 'm' in sesion_raw and 't' in sesion_raw:
                sesion = 'B'
            elif 'm' in sesion_raw:
                sesion = 'M'
            elif 't' in sesion_raw:
                sesion = 'T'
            else:
                sesion = 'M'

            # Convertir fecha teórica
            try:
                fecha_teorico = datetime.strptime(
                    datos['fecha_teorico'], '%d/%m/%y').date()
            except ValueError:
                fecha_teorico = None

            # Crear zona si no existe
            zona, _ = Zona.objects.get_or_create(
                nombre__iexact=zona_nombre, defaults={'nombre': zona_nombre})

            # Separar nombre
            partes = nombre.split()
            first_name = partes[0]
            last_name = ' '.join(partes[1:]) if len(partes) > 1 else ''

            if User.objects.filter(username=telefono).exists():
                self.stdout.write(self.style.WARNING(
                    f"⚠️ Usuario con teléfono {telefono} ya existe."))
                continue

            user = User.objects.create_user(
                username=telefono,
                first_name=first_name,
                last_name=last_name,
                password=telefono,
                rol=User.Roles.ALUMNO
            )

            alumno = Alumno.objects.create(usuario=user)

            Solicitud.objects.create(
                alumno=alumno,
                zona=zona,
                permiso=permiso,
                sesion_preferida=sesion,
                fecha_teorico=fecha_teorico,
                notas=notas
            )

            self.stdout.write(self.style.SUCCESS(
                f"✅ Alumno {user.get_full_name()} importado correctamente."))

        self.stdout.write(self.style.SUCCESS(
            '🎉 Proceso de importación finalizado.'))

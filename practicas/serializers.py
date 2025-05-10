from rest_framework import serializers
from django.contrib.auth.models import User
from citas.models import Profesor
from .models import Zona, Solicitud, SalidaDisponible, Reserva


class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = ['id', 'nombre']


class SolicitudSerializer(serializers.ModelSerializer):
    zona = serializers.PrimaryKeyRelatedField(queryset=Zona.objects.all(), write_only=True)
    zona_nombre = serializers.ReadOnlyField(source='zona.nombre')
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Solicitud
        fields = [
            'id', 'nombre', 'telefono', 'zona', 'zona_nombre', 'sesion_preferida',
            'fecha_teorico', 'fecha_inscripcion', 'notas', 'estado', 'estado_display'
        ]
        read_only_fields = ['zona_nombre', 'estado_display']


class SalidaDisponibleSerializer(serializers.ModelSerializer):
    profesor = serializers.PrimaryKeyRelatedField(queryset=Profesor.objects.all())
    zona = serializers.PrimaryKeyRelatedField(queryset=Zona.objects.all())
    profesor_username = serializers.ReadOnlyField(source='profesor.usuario.username')
    cupo_disponible = serializers.SerializerMethodField()

    class Meta:
        model = SalidaDisponible
        fields = [
            'id', 'profesor', 'profesor_username', 'zona', 'fecha', 'sesion',
            'cupo_maximo', 'cupo_disponible'
        ]

    def get_cupo_disponible(self, obj):
        return max(obj.cupo_maximo - obj.reservas.filter(estado__in=['P','C','I']).count(), 0)


class ReservaSerializer(serializers.ModelSerializer):
    alumno = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    alumno_username = serializers.ReadOnlyField(source='alumno.username')
    salida = serializers.PrimaryKeyRelatedField(queryset=SalidaDisponible.objects.all())
    salida_detalle = SalidaDisponibleSerializer(source='salida', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id', 'alumno', 'alumno_username', 'salida', 'salida_detalle',
            'estado', 'estado_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['alumno_username', 'salida_detalle', 'estado_display']

    def validate(self, data):
        salida = data.get('salida')
        if Reserva.objects.filter(salida=salida, estado__in=['P','C','I']).count() >= salida.cupo_maximo:
            raise serializers.ValidationError("No quedan plazas disponibles en esta salida.")
        return data

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request.user, 'id'):
            validated_data['alumno'] = request.user
        return super().create(validated_data)

from rest_framework import serializers
from .models import Profesor, HorarioDisponible, ClasePractica


class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'


class HorarioDisponibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioDisponible
        fields = ['id', 'fecha_hora_inicio']  # El profesor se asigna en create()

    def validate(self, data):
        """Validar que el usuario que intenta crear el horario es un profesor"""
        request = self.context.get('request')
        if not request or not hasattr(request.user, 'profesor'):
            raise serializers.ValidationError("Solo los profesores pueden definir horarios.")
        return data

    def create(self, validated_data):
        """Asignar el profesor a partir del usuario autenticado"""
        request = self.context.get('request')
        profesor = request.user.profesor
        return HorarioDisponible.objects.create(profesor=profesor, **validated_data)


class ClasePracticaSerializer(serializers.ModelSerializer):
    alumno_username = serializers.CharField(source='alumno.username', read_only=True)
    fecha_hora_inicio = serializers.DateTimeField(source='horario.fecha_hora_inicio', read_only=True)

    class Meta:
        model = ClasePractica
        fields = ['id', 'alumno', 'alumno_username', 'horario', 'fecha_hora_inicio']

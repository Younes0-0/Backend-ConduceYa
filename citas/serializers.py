# Los serializers convierten los datos de los modelos en JSON, para que el frontend (Astro) pueda consumirlos a través de la API.
from rest_framework import serializers
from .models import Profesor, HorarioDisponible, ClasePractica

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'

class HorarioDisponibleSerializer(serializers.ModelSerializer):
    profesor = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 🔥 Asigna el profesor automáticamente

    class Meta:
        model = HorarioDisponible
        fields = ['id', 'fecha_hora_inicio', 'profesor']  # 🔥 Permitimos solo definir la fecha y hora

    def validate(self, data):
        """Validar que el usuario que intenta crear el horario es un profesor"""
        request = self.context.get('request')
        if not hasattr(request.user, 'profesor'):
            raise serializers.ValidationError("Solo los profesores pueden definir horarios.")
        return data
    
    
class ClasePracticaSerializer(serializers.ModelSerializer):
    alumno_username = serializers.CharField(source='alumno.username', read_only=True)
    fecha_hora_inicio = serializers.DateTimeField(source='horario.fecha_hora_inicio', read_only=True)

    class Meta:
        model = ClasePractica
        fields = ['id', 'alumno', 'alumno_username', 'horario', 'fecha_hora_inicio']

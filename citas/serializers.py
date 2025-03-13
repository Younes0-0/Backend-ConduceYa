# Los serializers convierten los datos de los modelos en JSON, para que el frontend (Astro) pueda consumirlos a través de la API.
from rest_framework import serializers
from .models import Profesor, HorarioDisponible, ClasePractica

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'

class HorarioDisponibleSerializer(serializers.ModelSerializer):
    disponible = serializers.SerializerMethodField()

    class Meta:
        model = HorarioDisponible
        fields = '__all__'

    def get_disponible(self, obj):
        return not ClasePractica.objects.filter(horario=obj).exists()
    
    
class ClasePracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasePractica
        fields = '__all__'

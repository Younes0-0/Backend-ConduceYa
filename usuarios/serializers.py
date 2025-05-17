from rest_framework import serializers
from .models import User, Profesor, Alumno


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo User.
    Maneja creación segura de usuarios y campos de solo lectura.
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'rol'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ProfesorSerializer(serializers.ModelSerializer):
    """
    Serializer para perfil de Profesor.
    """
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(rol=User.Roles.PROFESOR))

    class Meta:
        model = Profesor
        fields = ['id', 'usuario', 'permisos']
        read_only_fields = ['id']


class AlumnoSerializer(serializers.ModelSerializer):
    """
    Serializer para perfil de Alumno.
    """
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(rol=User.Roles.ALUMNO))

    class Meta:
        model = Alumno
        fields = ['id', 'usuario']
        read_only_fields = ['id']

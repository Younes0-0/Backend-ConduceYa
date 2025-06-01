from rest_framework import serializers

from .models import User, Profesor, Alumno


# ═══════════════════════════  USER  ════════════════════════════ #
class UserSerializer(serializers.ModelSerializer):
    """Serializador de usuarios con manejo seguro de contraseña."""

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "rol",
        )
        read_only_fields = ("id",)

    # ---------- CREATE ----------------------------------------- #
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    # ---------- UPDATE ----------------------------------------- #
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# ═════════════════════════  MIXIN PERFILES  ═════════════════════ #
class _ProfileSerializerMixin(serializers.ModelSerializer):
    """Mixin reutilizable para Alumno y Profesor."""

    usuario = UserSerializer(required=False)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source="usuario",
        required=False,
    )

    def validate(self, attrs):
        if "usuario" not in attrs and "usuario_id" not in attrs:
            raise serializers.ValidationError(
                "Debes enviar 'usuario' o 'usuario_id'.")
        return attrs

    def _create_with_role(self, validated_data, rol):
        user_data_or_instance = validated_data.pop("usuario", None)

        # Si llega dict → crear usuario
        if isinstance(user_data_or_instance, dict):
            user_data_or_instance["rol"] = rol
            user = UserSerializer().create(user_data_or_instance)
        else:
            user = user_data_or_instance  # instancia o None
            if user is None:
                raise serializers.ValidationError(
                    {"usuario_id": "ID de usuario requerido."})
            if user.rol != rol:
                raise serializers.ValidationError(
                    {"usuario_id": f"El usuario no tiene rol '{rol}'."})

        return self.Meta.model.objects.create(usuario=user, **validated_data)


# ═════════════════════════  PROFESOR  ═══════════════════════════ #
class ProfesorSerializer(_ProfileSerializerMixin):
    class Meta:
        model = Profesor
        fields = (
            "id",
            "usuario",
            "usuario_id",
            "permisos",
        )
        read_only_fields = ("id", "usuario")

    def create(self, validated_data):
        return self._create_with_role(validated_data, rol=User.Roles.PROFESOR)


# ═════════════════════════  ALUMNO  ═════════════════════════════ #
class AlumnoSerializer(_ProfileSerializerMixin):
    class Meta:
        model = Alumno
        fields = (
            "id",
            "usuario",
            "usuario_id",
        )
        read_only_fields = ("id", "usuario")

    def create(self, validated_data):
        return self._create_with_role(validated_data, rol=User.Roles.ALUMNO)

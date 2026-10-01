"""Serializers de la app de autenticación JWT."""
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Producto


class UserSerializer(serializers.ModelSerializer):
    """Serie el usuario autenticado (para /me y /register)."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    """Crea un usuario nuevo. Requiere username + password."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # nunca guardar la contraseña en texto plano
        user.save()
        return user


class ProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Producto
        fields = (
            'codigo',
            'nombre',
            'descripcion',
            'imagen',
            'cantidad_disponible',
            'precio',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')
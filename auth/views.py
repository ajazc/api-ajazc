"""Vistas de la app de autenticación JWT.

- POST /api/auth/login/    -> {access, refresh}  (credenciales del usuario)
- POST /api/auth/refresh/  -> renueva el access token con el refresh
- GET  /api/auth/me/       -> datos del usuario autenticado (ruta protegida)
- POST /api/auth/register/ -> crea un usuario nuevo
"""
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Producto
from .serializers import ProductoSerializer, RegisterSerializer, UserSerializer


class LoginView(TokenObtainPairView):
    """
    Recibe username/email? (username) + password y devuelve:
    { "access": "<jwt>", "refresh": "<jwt>" }
    """
    # El serializer por defecto de SimpleJWT ya devuelve access + refresh.
    pass


class TokenRefreshViewCustom(TokenRefreshView):
    """Recibe { "refresh": "<jwt>" } y devuelve un access token nuevo."""
    pass


class MeView(generics.RetrieveAPIView):
    """Ruta protegida: devuelve los datos del usuario del JWT (Authorization: Bearer <access>)."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    """Crea un usuario nuevo y lo deja listo para hacer login."""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProductoListCreateView(generics.ListCreateAPIView):
    """Lista productos o crea uno nuevo."""
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Producto.objects.all()


class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Consulta, actualiza o elimina un producto por su codigo."""
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'codigo'

    def get_queryset(self):
        return Producto.objects.all()
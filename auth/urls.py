"""Rutas de autenticación JWT (app `auth`)."""
from django.urls import path

from .views import (
    LoginView,
    MeView,
    ProductoDetailView,
    ProductoEditView,
    ProductoListCreateView,
    RegisterView,
    TokenRefreshViewCustom,
)

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshViewCustom.as_view(), name='refresh'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('productos/', ProductoListCreateView.as_view(), name='producto-list'),
    path('productos/<str:codigo>/', ProductoDetailView.as_view(), name='producto-detail'),
    path('productos/<str:codigo>/editar/', ProductoEditView.as_view(), name='producto-edit'),
]
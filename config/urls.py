"""
URL configuration for config project.

Rutas:
- /admin/         Panel de administración de Django
- /api/auth/      Autenticación JWT (register, login, refresh, me)
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('auth.urls')),
]
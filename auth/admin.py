from django.contrib import admin

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'nombre', 'cantidad_disponible', 'precio', 'updated_at')
	search_fields = ('codigo', 'nombre')

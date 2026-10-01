from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
	codigo = models.CharField(max_length=20, primary_key=True)
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(null=True, blank=True)
	cantidad_disponible = models.PositiveIntegerField(default=0)
	precio = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		default=Decimal('0.00'),
		validators=[MinValueValidator(Decimal('0.00'))],
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'productos'
		ordering = ['codigo']

	def __str__(self):
		return f'{self.codigo} - {self.nombre}'

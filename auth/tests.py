from decimal import Decimal
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Producto


class ProductoApiTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='producto_test', password='test-password-123')
		self.client.force_authenticate(self.user)

	def test_list_and_create_product(self):
		response = self.client.post(
			'/api/productos/',
			{
				'codigo': 'PROD-001',
				'nombre': 'Producto de prueba',
				'descripcion': 'Descripcion de prueba',
				'cantidad_disponible': 10,
				'precio': '12.50',
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['codigo'], 'PROD-001')
		self.assertEqual(Producto.objects.get(codigo='PROD-001').precio, Decimal('12.50'))

		response = self.client.get('/api/productos/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data['results']), 1)

	def test_product_detail_update_and_delete(self):
		Producto.objects.create(codigo='PROD-002', nombre='Inicial', precio=Decimal('5.00'))

		response = self.client.patch(
			'/api/productos/PROD-002/',
			{'cantidad_disponible': 4},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['cantidad_disponible'], 4)

		response = self.client.delete('/api/productos/PROD-002/')

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Producto.objects.filter(codigo='PROD-002').exists())

	def test_product_can_store_image(self):
		buffer = BytesIO()
		Image.new('RGB', (1, 1), color='white').save(buffer, format='PNG')
		buffer.seek(0)
		image = SimpleUploadedFile(
			'name.png',
			buffer.read(),
			content_type='image/png',
		)

		response = self.client.post(
			'/api/productos/',
			{
				'codigo': 'PROD-003',
				'nombre': 'Producto con imagen',
				'cantidad_disponible': 2,
				'precio': '9.99',
				'imagen': image,
			},
			format='multipart',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('imagen', response.data)
		self.assertTrue(Producto.objects.get(codigo='PROD-003').imagen)

	def test_product_list_and_detail_are_public(self):
		Producto.objects.create(codigo='PROD-004', nombre='Publico', descripcion='Visible', precio=Decimal('7.00'))
		self.client.force_authenticate(user=None)

		response = self.client.get('/api/productos/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertGreaterEqual(len(response.data['results']), 1)

		response = self.client.get('/api/productos/PROD-004/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['descripcion'], 'Visible')

	def test_edit_endpoint_updates_product_data(self):
		Producto.objects.create(codigo='PROD-005', nombre='Antes', descripcion='Viejo', cantidad_disponible=1, precio=Decimal('10.00'))
		buffer = BytesIO()
		Image.new('RGB', (2, 2), color='black').save(buffer, format='PNG')
		buffer.seek(0)
		image = SimpleUploadedFile('edited.png', buffer.read(), content_type='image/png')

		response = self.client.patch(
			'/api/productos/PROD-005/editar/',
			{
				'nombre': 'Nuevo nombre',
				'descripcion': 'Descripcion actualizada',
				'cantidad_disponible': 8,
				'precio': '25.50',
				'imagen': image,
			},
			format='multipart',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['nombre'], 'Nuevo nombre')
		self.assertEqual(response.data['descripcion'], 'Descripcion actualizada')
		self.assertEqual(response.data['cantidad_disponible'], 8)
		self.assertEqual(response.data['precio'], '25.50')
		self.assertIn('imagen', response.data)

	def test_product_endpoints_require_authentication_for_write(self):
		self.client.force_authenticate(user=None)

		response = self.client.post('/api/productos/', {'codigo': 'PROD-006', 'nombre': 'No permitido', 'precio': '1.00'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		response = self.client.patch('/api/productos/PROD-005/editar/', {'nombre': 'No permitido'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

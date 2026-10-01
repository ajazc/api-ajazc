# API Ajazc

API REST construida con Django + Django REST Framework + JWT.

## Requisitos

- Python 3.12+
- Virtualenv o venv
- PostgreSQL/MySQL opcional (por defecto usa SQLite en desarrollo)

## Instalación

```bash
python -m venv .venv
. .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
```

## Crear un usuario válido

```bash
python manage.py createsuperuser
```

También podés crear usuarios por la API usando el endpoint de registro:

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "email": "demo@example.com",
    "password": "demo12345",
    "first_name": "Demo",
    "last_name": "User"
  }'
```

## Iniciar el servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

## Conectar con credenciales válidas

### 1) Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "password": "demo12345"
  }'
```

Respuesta esperada:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### 2) Usar el token JWT

Incluí el access token en el header `Authorization`:

```bash
curl http://localhost:8000/api/productos/ \
  -H "Authorization: Bearer <access_token>"
```

## Endpoints

### Autenticación

- `POST /api/auth/register/`
  - Crea un usuario nuevo
- `POST /api/auth/login/`
  - Devuelve `access` y `refresh`
- `POST /api/auth/refresh/`
  - Recibe `{ "refresh": "<token>" }` y devuelve un nuevo `access`
- `GET /api/auth/me/`
  - Devuelve el usuario autenticado

### Productos

- `GET /api/productos/`
  - Lista todos los productos
- `POST /api/productos/`
  - Crea un producto nuevo
- `GET /api/productos/<codigo>/`
  - Detalle de un producto
- `PATCH /api/productos/<codigo>/`
  - Actualiza un producto
- `DELETE /api/productos/<codigo>/`
  - Elimina un producto

### Ejemplo de creación de producto con imagen

```bash
curl -X POST http://localhost:8000/api/productos/ \
  -H "Authorization: Bearer <access_token>" \
  -F "codigo=PROD-100" \
  -F "nombre=Notebook" \
  -F "descripcion=Notebook gamer 15 pulgadas" \
  -F "cantidad_disponible=10" \
  -F "precio=1299.99" \
  -F "imagen=@/ruta/a/tu-imagen.jpg"
```

Respuesta tipo:

```json
{
  "codigo": "PROD-100",
  "nombre": "Notebook",
  "descripcion": "Notebook gamer 15 pulgadas",
  "imagen": "http://localhost:8000/media/productos/tu-imagen.jpg",
  "cantidad_disponible": 10,
  "precio": "1299.99",
  "created_at": "2026-10-01T00:00:00-03:00",
  "updated_at": "2026-10-01T00:00:00-03:00"
}
```

## Archivos multimedia

Las imágenes subidas se almacenan en la carpeta `media/productos/` y se sirven automáticamente en desarrollo desde:

```text
http://localhost:8000/media/...
```

## Variables de entorno

Podés copiar el ejemplo desde [`.env.example`](.env.example) y completar los valores necesarios.

## Seguridad

- No commitear `.env`
- No guardar secretos en el repositorio
- Las contraseñas se almacenan hasheadas por Django

from django.apps import AppConfig


class AuthConfig(AppConfig):
    """Config de la app `auth`.

    La carpeta se llama `auth` (como pidió el cliente), pero su `label`
    es `auth_api` para no chocar con `django.contrib.auth`,
    que ya usa el label `auth`.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth'
    label = 'auth_api'
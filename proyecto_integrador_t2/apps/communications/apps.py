from django.apps import AppConfig


class MessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.communications'
    def ready(self):
            import apps.communications.signals  # Importar señales para que se registren
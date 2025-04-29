from django.apps import AppConfig


class PosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Pos'


    def ready(self):
        import Pos.signals  # Import your signals here

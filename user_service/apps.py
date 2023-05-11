from django.apps import AppConfig


class UserServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_service'

    def ready(self):
        import user_service.signals

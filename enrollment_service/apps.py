from django.apps import AppConfig


class EnrollmentServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'enrollment_service'

    def ready(self) -> None:
        import enrollment_service.signals
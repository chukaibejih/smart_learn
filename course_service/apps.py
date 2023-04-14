from django.apps import AppConfig


class CourseServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'course_service'

    def ready(self):
        import course_service.signals
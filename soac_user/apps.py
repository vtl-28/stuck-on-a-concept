from django.apps import AppConfig


class StackusersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'soac_user'

    def ready(self):
        import soac_user.signals

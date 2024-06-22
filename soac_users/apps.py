from django.apps import AppConfig


class SoacUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'soac_users'

    # def ready(self):
    #     import soac_users.signals
from django.apps import AppConfig


class SendnotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sendNotification'

    def ready(self):
        import sendNotification.signals

from django.apps import AppConfig


class PaypalIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paypal_integration'

    def ready(self):
        import paypal_integration.hooks
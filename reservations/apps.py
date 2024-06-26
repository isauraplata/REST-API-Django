from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'

    def ready(self):
        import reservations.signals

    @staticmethod
    def on_post_migrate(sender, **kwargs):
        # Obtiene la clase Reservation usando la función get_model de apps
        Reservation = apps.get_model('reservations', 'Reservation')

        content_type = apps.get_model('contenttypes.ContentType')
        if not content_type.objects.filter(app_label='reservations', model='reservation').exists():
            Reservation.create_custom_permissions()

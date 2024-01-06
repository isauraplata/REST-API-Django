from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'

    def ready(self):
        import reservations.signals
        # Registra el receptor de la señal post_migrate
        #post_migrate.connect(self.on_post_migrate, sender=self)

    @staticmethod
    def on_post_migrate(sender, **kwargs):
        # Obtiene la clase Reservation usando la función get_model de apps
        Reservation = apps.get_model('reservations', 'Reservation')

        # Verifica si ContentType ya está creado antes de llamar a create_custom_permissions
        content_type = apps.get_model('contenttypes.ContentType')
        if not content_type.objects.filter(app_label='reservations', model='reservation').exists():
            Reservation.create_custom_permissions()

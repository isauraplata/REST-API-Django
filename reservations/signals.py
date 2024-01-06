# reservations/signals.py
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Reservation

@receiver(post_migrate)
def on_post_migrate(sender, **kwargs):
    Reservation = apps.get_model('reservations', 'Reservation')

    # Verifica si ContentType ya está creado antes de llamar a create_custom_permissions
    content_type = apps.get_model('contenttypes.ContentType')
    if not content_type.objects.filter(app_label='reservations', model='reservation').exists():
        Reservation.create_custom_permissions()

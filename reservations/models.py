from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone


class CustomPermissions:
    CAN_CREATE_RESERVATION = 'can_create_reservation'
    CAN_DELETE_RESERVATION = 'can_delete_reservation'
    CAN_UPDATE_RESERVATION = 'can_update_reservation'


class Reservation(models.Model):
    customer = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=200, blank=True)
    customer_email = models.CharField(max_length=200, default='', blank=False, null=False)
    special_notes = models.TextField(max_length=1000, blank=True)
    reservation_date = models.DateTimeField(default=timezone.now)
    location = models.TextField(max_length=1000, blank=True)
    hour = models.TimeField(blank=True, default='12:00')
    num_people = models.IntegerField(default=2)
    STATUS_CHOICES = [
        ('confirmed', 'confirmed'),
        ('pending', 'pending'),
        ('cancelled', 'cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def create_custom_permissions(**kwargs):
        content_type = ContentType.objects.get_for_model(Reservation)

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_CREATE_RESERVATION,
            name='Can create reservation',
            content_type=content_type,
        )

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_DELETE_RESERVATION,
            name='Can delete reservation',
            content_type=content_type,
        )

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_UPDATE_RESERVATION,
            name='Can update reservation',
            content_type=content_type,
        )
        

@receiver(post_migrate)
def on_post_migrate(sender, **kwargs):
    Reservation.create_custom_permissions(**kwargs)
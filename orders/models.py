from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from menu.models import Dish


class CustomPermissions:
    CAN_CREATE_ORDER = 'can_create_order'
    CAN_DELETE_ORDER = 'can_delete_order'
    CAN_UPDATE_ORDER = 'can_update_order'

       
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name} in Order {self.id}"
    
    @staticmethod
    def create_custom_permissions(**kwargs):
        content_type = ContentType.objects.get_for_model(Order)

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_CREATE_ORDER,
            name='Can create order',
            content_type=content_type,
        )

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_DELETE_ORDER,
            name='Can delete order',
            content_type=content_type,
        )

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_UPDATE_ORDER,
            name='Can update order',
            content_type=content_type,
        )


# Conecta la señal post_migrate al método create_custom_permissions
@receiver(post_migrate)
def on_post_migrate(sender, **kwargs):
    Order.create_custom_permissions(**kwargs)
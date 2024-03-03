from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class CustomPermissions:
    CAN_CREATE_DISH = 'can_create_dish'
    CAN_DELETE_DISH = 'can_delete_dish'
    CAN_UPDATE_DISH = 'can_update_dish'


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    availability = models.BooleanField(default=True)
    ingredients = models.TextField()
    allergens = models.TextField(blank=True, null=True)
    cuisine_type = models.CharField(max_length=50)
    spice_level = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to="archivos/", default="default_image.jpg")
    image_path = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image_path:
            self.image_path = f'archivos/{self.image_path}'
        super().save(*args, **kwargs)


    @staticmethod
    def create_custom_permissions(**kwargs):
        content_type = ContentType.objects.get_for_model(Dish)

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_CREATE_DISH,
            name='Can create dish',
            content_type=content_type,
        )

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_DELETE_DISH,
            name='Can delete dish',
            content_type=content_type,
        )

        Permission.objects.get_or_create(
            codename=CustomPermissions.CAN_UPDATE_DISH,
            name='Can update dish',
            content_type=content_type,
        )
             

@receiver(post_migrate)
def on_post_migrate(sender, **kwargs):
    Dish.create_custom_permissions(**kwargs)
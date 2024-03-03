from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    
    def ready(self):
        import orders.signals

    @staticmethod
    def on_post_migrate(sender, **kwargs):
        Order = apps.get_model('orders', 'Order')
        content_type = apps.get_model('contenttypes.ContentType')
        if not content_type.objects.filter(app_label='orders', model='order').exists():
            Order.create_custom_permissions()


# Generated by Django 4.2.7 on 2024-01-06 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_remove_dish_image_dish_image_path_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-28 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_yahir'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Yahir',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='user_id',
            new_name='user',
        ),
    ]

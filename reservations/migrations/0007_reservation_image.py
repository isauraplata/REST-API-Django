# Generated by Django 4.2.7 on 2023-12-09 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0006_reservation_num_people_reservation_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='archivos/'),
        ),
    ]
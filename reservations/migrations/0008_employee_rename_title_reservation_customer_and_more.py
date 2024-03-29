# Generated by Django 4.2.7 on 2023-12-31 03:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0007_reservation_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('hire_date', models.DateField()),
                ('position', models.CharField(max_length=100)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('hours_worked', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='title',
            new_name='customer',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='available',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='description',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='image',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='price',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='reservation_type',
        ),
        migrations.AddField(
            model_name='reservation',
            name='customer_email',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='reservation',
            name='customer_phone',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='reservation',
            name='hour',
            field=models.TimeField(blank=True, default='12:00'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='reservation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='reservation',
            name='special_notes',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('confirmed', 'confirmed'), ('pending', 'pending'), ('cancelled', 'cancelled')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='location',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]

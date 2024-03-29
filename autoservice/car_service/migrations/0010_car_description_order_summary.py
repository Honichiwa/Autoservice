# Generated by Django 4.2.1 on 2023-06-06 10:16

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('car_service', '0009_car_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='description',
            field=tinymce.models.HTMLField(blank=True, max_length=8000, null=True, verbose_name='car_description'),
        ),
        migrations.AddField(
            model_name='order',
            name='summary',
            field=tinymce.models.HTMLField(blank=True, max_length=8000, null=True, verbose_name='order_summary'),
        ),
    ]

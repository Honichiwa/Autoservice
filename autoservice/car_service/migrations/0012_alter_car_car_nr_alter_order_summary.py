# Generated by Django 4.2.1 on 2023-06-08 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_service', '0011_ordercomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_nr',
            field=models.CharField(max_length=20, verbose_name='car nr'),
        ),
        migrations.AlterField(
            model_name='order',
            name='summary',
            field=models.TextField(blank=True, max_length=8000, null=True, verbose_name='order_summary'),
        ),
    ]

# Generated by Django 5.0.7 on 2024-10-30 09:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_cartitems_updated_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='quantity',
            field=models.IntegerField(default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
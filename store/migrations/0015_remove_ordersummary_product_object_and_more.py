# Generated by Django 5.0.7 on 2024-11-08 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_delete_address_ordersummary_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordersummary',
            name='product_object',
        ),
        migrations.AddField(
            model_name='ordersummary',
            name='cart_item_object',
            field=models.ManyToManyField(to='store.cartitems'),
        ),
    ]

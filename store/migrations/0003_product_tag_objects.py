# Generated by Django 5.0.7 on 2024-10-10 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tag_objects',
            field=models.ManyToManyField(to='store.tag'),
        ),
    ]
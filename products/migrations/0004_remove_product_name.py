# Generated by Django 5.2.1 on 2025-05-31 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='name',
        ),
    ]

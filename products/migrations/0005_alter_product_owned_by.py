# Generated by Django 5.2.1 on 2025-06-03 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='owned_by',
            field=models.CharField(db_index=True, max_length=500),
        ),
    ]

# Generated by Django 5.1.2 on 2025-05-28 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmeticapp', '0005_rename_product_order_productid_remove_cart_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=100),
        ),
    ]

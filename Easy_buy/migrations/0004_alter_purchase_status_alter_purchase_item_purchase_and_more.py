# Generated by Django 5.1.6 on 2025-03-25 09:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Easy_buy', '0003_remove_order_created_at_alter_purchase_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('delivered', 'delivered'), ('cancelled', 'cancelled')], default='pending', max_length=25),
        ),
        migrations.AlterField(
            model_name='purchase_item',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Easy_buy.purchase'),
        ),
        migrations.AlterField(
            model_name='purchasedelivery',
            name='status',
            field=models.CharField(choices=[('assigned', 'assigned'), ('delivered', 'delivered'), ('cancelled', 'cancelled')], default='pending', max_length=25),
        ),
    ]

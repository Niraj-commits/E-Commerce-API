# Generated by Django 5.1.6 on 2025-03-25 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Easy_buy', '0004_alter_purchase_status_alter_purchase_item_purchase_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasedelivery',
            name='status',
            field=models.CharField(choices=[('assigned', 'assigned'), ('delivered', 'delivered'), ('cancelled', 'cancelled')], default='assigned', max_length=25),
        ),
    ]

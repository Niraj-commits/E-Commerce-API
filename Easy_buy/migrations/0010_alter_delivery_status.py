# Generated by Django 5.1.6 on 2025-03-11 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Easy_buy', '0009_remove_orderitem_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(choices=[('assigned', 'assigned'), ('delivered', 'delivered'), ('cancelled', 'cancelled')], default='assigned', max_length=25),
        ),
    ]

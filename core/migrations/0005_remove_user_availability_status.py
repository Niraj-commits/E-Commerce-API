# Generated by Django 5.1.6 on 2025-03-12 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_user_address_alter_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='availability_status',
        ),
    ]

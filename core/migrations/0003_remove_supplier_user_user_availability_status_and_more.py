# Generated by Django 5.1.6 on 2025-03-10 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_supplierprofile_user_deliveryperson_supplier_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='availability_status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='company_name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='license_no',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='vehicle_type',
            field=models.CharField(blank=True, choices=[('scooter', 'scooter'), ('bike', 'bike')], default='bike', max_length=25, null=True),
        ),
        migrations.DeleteModel(
            name='DeliveryPerson',
        ),
        migrations.DeleteModel(
            name='Supplier',
        ),
    ]

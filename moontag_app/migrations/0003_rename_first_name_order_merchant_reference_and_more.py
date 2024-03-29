# Generated by Django 4.2.7 on 2024-01-14 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moontag_app', '0002_order_first_name_order_last_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='first_name',
            new_name='merchant_reference',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='last_name',
            new_name='transaction_tracking_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='mpesa_transaction_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone_number',
        ),
    ]

# Generated by Django 4.2.7 on 2024-01-01 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moontag_app', '0010_product_is_data3'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_data2',
            field=models.BooleanField(default=False),
        ),
    ]
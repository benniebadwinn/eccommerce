# Generated by Django 4.2.7 on 2023-12-31 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moontag_app', '0007_alter_productattribute_discountprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='moontag_app.productattribute'),
        ),
    ]

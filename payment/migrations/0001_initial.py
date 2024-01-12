# Generated by Django 4.2.7 on 2024-01-12 04:41

from django.db import migrations, models
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=200000)),
                ('description', models.CharField(default='product/service purchased', max_length=100)),
                ('type', models.CharField(default='MERCHANT', max_length=9)),
                ('reference', models.CharField(max_length=6)),
            ],
        ),
    ]

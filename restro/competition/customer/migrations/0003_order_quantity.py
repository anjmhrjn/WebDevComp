# Generated by Django 3.1.4 on 2020-12-09 17:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20201209_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
    ]
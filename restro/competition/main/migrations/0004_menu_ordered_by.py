# Generated by Django 3.1.4 on 2020-12-04 08:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_auto_20201204_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='ordered_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]

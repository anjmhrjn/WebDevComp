# Generated by Django 3.1.4 on 2020-12-04 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_menu_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='ordered_by',
        ),
    ]

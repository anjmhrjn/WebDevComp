# Generated by Django 3.1.4 on 2020-12-04 08:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0007_remove_menu_ordered_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='ordered_by',
            field=models.ManyToManyField(through='main.Order', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='menu',
            name='item_type',
            field=models.CharField(choices=[('food', 'FOOD'), ('dessert', 'DESSERT'), ('drink', 'DRINK')], default='food', max_length=8),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('delivered', 'DELIVERED'), ('canceled', 'CANCELED'), ('in process', 'IN PROCESS'), ('preparing', 'PREPARING')], default='in process', max_length=12),
        ),
    ]

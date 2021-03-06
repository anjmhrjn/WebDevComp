# Generated by Django 3.1.4 on 2020-12-19 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_order_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('delivered', 'DELIVERED'), ('cancelled', 'CANCELED'), ('in process', 'IN PROCESS'), ('processed', 'PROCESSED')], default='in process', max_length=12),
        ),
    ]

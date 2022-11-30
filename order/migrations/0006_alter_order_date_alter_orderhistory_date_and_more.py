# Generated by Django 4.1 on 2022-11-30 16:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 30, 21, 54, 58, 49032), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 30, 21, 54, 58, 50041), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='orderproducts',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='order.order'),
        ),
    ]

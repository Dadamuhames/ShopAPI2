# Generated by Django 4.1 on 2022-12-18 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0058_alter_order_adres_alter_order_city_alter_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 18, 22, 6, 10, 621382), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 18, 22, 6, 10, 621382), verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 18, 17, 6, 10, 622392, tzinfo=datetime.timezone.utc), verbose_name='Date'),
        ),
    ]
# Generated by Django 4.1 on 2022-12-07 19:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0036_delete_orderstatus_alter_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 8, 0, 14, 1, 323600), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 8, 0, 14, 1, 323600), verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 19, 14, 1, 323600, tzinfo=datetime.timezone.utc), verbose_name='Date'),
        ),
    ]

# Generated by Django 4.1 on 2022-12-09 07:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0049_alter_order_date_alter_order_update_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 12, 12, 51, 167936), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 12, 12, 51, 167936), verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 7, 12, 51, 167936, tzinfo=datetime.timezone.utc), verbose_name='Date'),
        ),
    ]

# Generated by Django 4.1 on 2022-12-09 06:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0045_alter_order_date_alter_order_update_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 11, 55, 35, 949209), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 11, 55, 35, 949209), verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 6, 55, 35, 950208, tzinfo=datetime.timezone.utc), verbose_name='Date'),
        ),
    ]
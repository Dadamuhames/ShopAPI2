# Generated by Django 4.1 on 2022-12-21 13:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0073_orderaplication_last_name_orderaplication_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 21, 18, 30, 3, 751552), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 21, 18, 30, 3, 751552), verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 21, 13, 30, 3, 752468, tzinfo=datetime.timezone.utc), verbose_name='Date'),
        ),
    ]

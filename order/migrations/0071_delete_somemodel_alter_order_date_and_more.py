# Generated by Django 4.1 on 2022-12-21 13:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0070_alter_order_date_alter_order_update_date_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SomeModel',
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 21, 18, 26, 9, 449096), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 21, 18, 26, 9, 449096), verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 21, 13, 26, 9, 450092, tzinfo=datetime.timezone.utc), verbose_name='Date'),
        ),
    ]

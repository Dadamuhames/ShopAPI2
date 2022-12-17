# Generated by Django 4.1 on 2022-12-17 13:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0057_alter_order_date_alter_order_update_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='adres',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Adres'),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='order.city'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 17, 18, 14, 37, 190193), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='order.state'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Ожидание', 'Ожидание'), ('Ожидание модерации', 'Ожидание модерации'), ('Ожидание сборки', 'Ожидание сборки'), ('На доставке', 'На доставке'), ('Отменено', 'Отменено'), ('Доставлено', 'Доставлено')], default='Ожидание', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='order',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 17, 18, 14, 37, 190193), verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 17, 13, 14, 37, 190193, tzinfo=datetime.timezone.utc), verbose_name='Date'),
        ),
    ]

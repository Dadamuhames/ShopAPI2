# Generated by Django 4.1 on 2022-11-30 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='session',
        ),
    ]

# Generated by Django 4.1 on 2022-12-09 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_remove_products_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='popular',
            field=models.BooleanField(default=False, verbose_name='Popular'),
        ),
    ]

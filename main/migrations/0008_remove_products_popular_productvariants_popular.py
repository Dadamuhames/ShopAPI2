# Generated by Django 4.1 on 2022-11-24 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_category_popular'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='popular',
        ),
        migrations.AddField(
            model_name='productvariants',
            name='popular',
            field=models.BooleanField(default=False, verbose_name='Popular'),
        ),
    ]
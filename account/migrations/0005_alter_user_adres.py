# Generated by Django 4.1 on 2022-11-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_avatar_alter_user_city_alter_user_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='adres',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Adres'),
        ),
    ]
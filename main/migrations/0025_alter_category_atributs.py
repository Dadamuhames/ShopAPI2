# Generated by Django 4.1 on 2022-12-07 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_category_atributs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='atributs',
            field=models.ManyToManyField(blank=True, null=True, to='main.atributs'),
        ),
    ]
# Generated by Django 4.1 on 2022-12-07 19:37

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_category_atributs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='category_icons'),
        ),
    ]

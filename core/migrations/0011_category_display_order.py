# Generated by Django 2.0.2 on 2018-03-21 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20180321_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='display_order',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]

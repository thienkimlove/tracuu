# Generated by Django 2.0.2 on 2018-03-21 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20180321_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_static',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 2.0.2 on 2018-03-15 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20180315_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]

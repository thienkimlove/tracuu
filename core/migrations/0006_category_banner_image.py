# Generated by Django 2.0.2 on 2018-03-19 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20180319_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='banner_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
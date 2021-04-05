# Generated by Django 3.1.7 on 2021-04-05 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_auto_20210405_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='playdate',
            name='location',
            field=models.CharField(default='Home', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='Hello', max_length=300),
        ),
    ]
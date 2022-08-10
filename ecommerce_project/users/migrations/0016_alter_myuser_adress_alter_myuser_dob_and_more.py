# Generated by Django 4.0.4 on 2022-08-10 08:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_myuser_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='adress',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='dob',
            field=models.DateField(blank=True, default=datetime.date(2022, 8, 10)),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='gender',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]

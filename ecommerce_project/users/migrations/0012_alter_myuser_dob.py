# Generated by Django 4.0.4 on 2022-07-29 09:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_myuser_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='dob',
            field=models.DateField(blank=True, default=datetime.date(2022, 7, 29)),
        ),
    ]

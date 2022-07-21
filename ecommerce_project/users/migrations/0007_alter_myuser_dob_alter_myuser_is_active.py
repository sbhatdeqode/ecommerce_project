# Generated by Django 4.0.4 on 2022-07-21 05:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_myuser_shop_name_myuser_shop_type_alter_myuser_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='dob',
            field=models.DateField(blank=True, default=datetime.date(2022, 7, 21)),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.0.4 on 2022-07-26 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=4, max_length=5),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

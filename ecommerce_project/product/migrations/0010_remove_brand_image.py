# Generated by Django 4.0.4 on 2022-07-27 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_category_rename_size_material_alter_brand_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='image',
        ),
    ]

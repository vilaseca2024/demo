# Generated by Django 4.2 on 2024-12-06 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0010_carnet_file_cartapresentacion_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clasificacionfile',
            name='siglas',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]

# Generated by Django 4.2 on 2025-03-07 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0151_calendario_activo_calendario_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendario',
            name='activo',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='calendario',
            name='estado',
            field=models.BooleanField(default=True, null=True),
        ),
    ]

# Generated by Django 4.2 on 2025-01-17 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0075_remove_bajacorreosusuarios_correo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bajacorreosusuarios',
            name='correo',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='bajacorreosusuarios',
            name='correo_alt',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

# Generated by Django 4.2 on 2025-01-09 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0050_rename_imagen_6_equipos_imagen_0'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipos',
            name='codigo_equipo',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

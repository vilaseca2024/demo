# Generated by Django 4.2 on 2025-01-09 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0055_alter_asignacion_equipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipos',
            name='estado',
            field=models.BooleanField(default=True, null=True),
        ),
    ]

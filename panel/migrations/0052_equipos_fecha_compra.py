# Generated by Django 4.2 on 2025-01-09 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0051_equipos_codigo_equipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipos',
            name='fecha_compra',
            field=models.DateField(null=True),
        ),
    ]

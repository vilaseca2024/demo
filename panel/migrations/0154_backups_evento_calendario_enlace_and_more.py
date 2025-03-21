# Generated by Django 5.1.7 on 2025-03-12 18:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0153_backupsistemas_ubicacion_gastos'),
    ]

    operations = [
        migrations.AddField(
            model_name='backups',
            name='evento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.calendario'),
        ),
        migrations.AddField(
            model_name='calendario',
            name='enlace',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='calendario',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.areas'),
        ),
    ]

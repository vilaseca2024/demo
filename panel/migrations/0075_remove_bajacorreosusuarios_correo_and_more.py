# Generated by Django 4.2 on 2025-01-17 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0074_remove_asignacioncorreosusuarios_correo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bajacorreosusuarios',
            name='correo',
        ),
        migrations.AddField(
            model_name='asignacioncorreosusuarios',
            name='correo',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usuariocorreos',
            name='asignado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.asignacioncorreosusuarios'),
        ),
    ]

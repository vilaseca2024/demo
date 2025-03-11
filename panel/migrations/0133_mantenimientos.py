# Generated by Django 4.2 on 2025-02-14 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0132_calendario_area_calendario_usuario_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mantenimientos',
            fields=[
                ('id_mantenimiento', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_planificada', models.DateTimeField(null=True)),
                ('fecha_realizada', models.DateTimeField(null=True)),
                ('fecha_culminada', models.DateTimeField(null=True)),
                ('evaluacion_inicial', models.CharField(max_length=250, null=True)),
                ('observaciones', models.CharField(max_length=200, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('correo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.usuariocorreos')),
                ('equipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.equipos')),
                ('estado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.estadobackupscorreos')),
            ],
            options={
                'db_table': 'mantenimiento',
            },
        ),
    ]

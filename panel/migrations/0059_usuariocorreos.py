# Generated by Django 4.2 on 2025-01-13 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel', '0058_devolucionequipo_empleado_devolucionequipo_equipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='usuarioCorreos',
            fields=[
                ('id_u_correo', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(null=True)),
                ('correo_usuario', models.CharField(max_length=50, null=True)),
                ('correo_alt', models.CharField(max_length=50, null=True)),
                ('descripcion', models.CharField(max_length=150, null=True)),
                ('tipo', models.CharField(max_length=10, null=True)),
                ('observacion', models.CharField(max_length=100, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('empleado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'usuario_correos',
            },
        ),
    ]

# Generated by Django 4.2 on 2024-12-12 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel', '0017_certificadoaprobados_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContratoEmpleado',
            fields=[
                ('id_datos_contrato', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_registro', models.DateField()),
                ('celular_trabajo', models.IntegerField(null=True)),
                ('whatsapp_trabajo', models.IntegerField(null=True)),
                ('numero_interno', models.IntegerField(null=True)),
                ('correo_corporativo', models.CharField(max_length=100, null=True)),
                ('estado_trabajador', models.CharField(max_length=20, null=True)),
                ('antiguedad', models.BooleanField(default=False)),
                ('inicio_contrato', models.DateField(null=True)),
                ('modalidad_trabajo', models.CharField(max_length=10)),
                ('activo', models.BooleanField(default=True)),
                ('clasificacion_anti', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.clasificacionanti')),
                ('id_empleado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tipo_contrato', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.tipocontrato')),
            ],
            options={
                'db_table': 'contrato_empleado',
            },
        ),
    ]

# Generated by Django 4.2 on 2025-01-23 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0082_equiposcuentas_observaciones'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotivoCambio',
            fields=[
                ('id_motivo', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'motivo_cambio_contrasena',
            },
        ),
    ]

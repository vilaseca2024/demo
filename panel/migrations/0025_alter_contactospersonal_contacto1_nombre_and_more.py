# Generated by Django 4.2.17 on 2024-12-18 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0024_certificados_id_dirigido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactospersonal',
            name='contacto1_nombre',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contactospersonal',
            name='contacto1_parentesco',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contactospersonal',
            name='contacto2_nombre',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contactospersonal',
            name='contacto2_numero',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='contactospersonal',
            name='contacto2_parentesco',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contactospersonal',
            name='direccion',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='contactospersonal',
            name='hijos',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='datospersonal',
            name='ap_paterno',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='datospersonal',
            name='correo',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='datospersonal',
            name='expedido',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='datospersonal',
            name='fecha_nacimiento',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='datospersonal',
            name='nombre',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='datospersonal',
            name='tipo_sangre',
            field=models.CharField(max_length=10, null=True),
        ),
    ]

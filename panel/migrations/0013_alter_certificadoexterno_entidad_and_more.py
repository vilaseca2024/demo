# Generated by Django 4.2 on 2024-12-06 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0012_alter_convenioscontratos_fecha_emision_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificadoexterno',
            name='entidad',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='certificadoexterno',
            name='tiempo',
            field=models.IntegerField(null=True),
        ),
    ]

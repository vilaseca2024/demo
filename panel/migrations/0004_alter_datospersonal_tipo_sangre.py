# Generated by Django 4.2 on 2024-11-25 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_departamento_expedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datospersonal',
            name='tipo_sangre',
            field=models.CharField(max_length=10),
        ),
    ]

# Generated by Django 4.2 on 2024-12-16 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0021_alter_modulo_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='permiso',
            name='agregar',
            field=models.BooleanField(default=False),
        ),
    ]

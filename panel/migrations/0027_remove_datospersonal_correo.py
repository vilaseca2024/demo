# Generated by Django 4.2 on 2024-12-20 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0026_foto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datospersonal',
            name='correo',
        ),
    ]

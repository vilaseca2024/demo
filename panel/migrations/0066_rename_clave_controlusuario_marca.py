# Generated by Django 4.2 on 2025-01-14 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0065_controlusuario_clave_controlusuario_tipo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='controlusuario',
            old_name='clave',
            new_name='marca',
        ),
    ]

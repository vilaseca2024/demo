# Generated by Django 4.2 on 2025-02-12 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0124_backupscorreos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backupscorreos',
            name='correo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.usuariocorreos'),
        ),
        migrations.AlterField(
            model_name='backupscorreos',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]

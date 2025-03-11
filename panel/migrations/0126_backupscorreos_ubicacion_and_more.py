# Generated by Django 4.2 on 2025-02-12 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0125_alter_backupscorreos_correo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='backupscorreos',
            name='ubicacion',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='backupscorreos',
            name='disco_duro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.discobackups'),
        ),
    ]

# Generated by Django 4.2 on 2025-02-10 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0122_rename_responsable_verificacionbackups_revisor_cambio'),
    ]

    operations = [
        migrations.AddField(
            model_name='backups',
            name='tipo_backup',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

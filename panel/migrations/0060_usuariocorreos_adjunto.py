# Generated by Django 4.2 on 2025-01-13 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0059_usuariocorreos'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariocorreos',
            name='adjunto',
            field=models.FileField(blank=True, null=True, upload_to='correos/'),
        ),
    ]

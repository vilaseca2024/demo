# Generated by Django 4.2 on 2025-01-07 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0037_alter_equipos_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipos',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='equipos/'),
        ),
        migrations.AddField(
            model_name='equipos',
            name='imagen_1',
            field=models.ImageField(blank=True, null=True, upload_to='equipos/'),
        ),
        migrations.AddField(
            model_name='equipos',
            name='imagen_2',
            field=models.ImageField(blank=True, null=True, upload_to='equipos/'),
        ),
        migrations.AddField(
            model_name='equipos',
            name='imagen_3',
            field=models.ImageField(blank=True, null=True, upload_to='equipos/'),
        ),
        migrations.AddField(
            model_name='equipos',
            name='imagen_4',
            field=models.ImageField(blank=True, null=True, upload_to='equipos/'),
        ),
    ]

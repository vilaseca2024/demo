# Generated by Django 4.2 on 2025-01-15 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0067_verificacioncodigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlusuario',
            name='anterior',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

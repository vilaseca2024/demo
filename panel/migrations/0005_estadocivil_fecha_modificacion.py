# Generated by Django 4.2 on 2024-11-25 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0004_alter_datospersonal_tipo_sangre'),
    ]

    operations = [
        migrations.AddField(
            model_name='estadocivil',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

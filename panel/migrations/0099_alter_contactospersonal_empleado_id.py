# Generated by Django 4.2 on 2025-01-29 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0098_alter_contactospersonal_empleado_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactospersonal',
            name='empleado_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.datospersonal'),
        ),
    ]

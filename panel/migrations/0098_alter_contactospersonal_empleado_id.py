# Generated by Django 4.2 on 2025-01-28 22:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel', '0097_alter_contactospersonal_empleado_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactospersonal',
            name='empleado_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

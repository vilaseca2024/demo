# Generated by Django 4.2 on 2025-02-14 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel', '0136_alter_mantenimientos_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='mantenimientos',
            name='encargado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

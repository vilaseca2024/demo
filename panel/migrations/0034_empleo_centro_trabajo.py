# Generated by Django 4.2 on 2024-12-30 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0033_clasificacionanti_rango_fin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleo',
            name='centro_trabajo',
            field=models.CharField(max_length=30, null=True),
        ),
    ]

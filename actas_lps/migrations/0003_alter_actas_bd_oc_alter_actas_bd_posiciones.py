# Generated by Django 5.0.1 on 2024-01-23 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actas_lps', '0002_delete_bd_actas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actas_bd',
            name='oc',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='actas_bd',
            name='posiciones',
            field=models.CharField(max_length=100),
        ),
    ]

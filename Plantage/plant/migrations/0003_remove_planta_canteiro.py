# Generated by Django 5.1.1 on 2024-10-02 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0002_alter_planta_canteiro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planta',
            name='canteiro',
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-02 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planta',
            name='canteiro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='plant.canteiro'),
        ),
    ]
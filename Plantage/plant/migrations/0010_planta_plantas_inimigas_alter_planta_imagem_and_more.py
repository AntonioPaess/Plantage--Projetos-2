# Generated by Django 5.1.1 on 2024-11-12 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0009_alter_canteiro_quantmaxplant'),
    ]

    operations = [
        migrations.AddField(
            model_name='planta',
            name='plantas_inimigas',
            field=models.ManyToManyField(blank=True, to='plant.planta'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='imagem',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='planta',
            name='necessidade_de_nutrientes',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='planta',
            name='nome',
            field=models.CharField(max_length=100),
        ),
    ]

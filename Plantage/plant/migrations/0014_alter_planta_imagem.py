# Generated by Django 5.1.1 on 2024-11-26 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0013_alter_planta_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planta',
            name='imagem',
            field=models.ImageField(upload_to='plantas/'),
        ),
    ]
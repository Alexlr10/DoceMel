# Generated by Django 2.1.7 on 2020-03-29 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='quantLote',
            field=models.IntegerField(blank=True, null=True, verbose_name='Quantidade'),
        ),
    ]
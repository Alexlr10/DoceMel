# Generated by Django 2.0 on 2020-04-09 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0004_auto_20200409_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balanco',
            name='Data',
        ),
        migrations.AddField(
            model_name='balanco',
            name='datas',
            field=models.DateField(blank=True, null=True, verbose_name='datas'),
        ),
    ]

# Generated by Django 2.1.7 on 2020-03-26 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='quantidade',
        ),
    ]

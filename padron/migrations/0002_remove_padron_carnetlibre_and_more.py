# Generated by Django 5.0.4 on 2024-10-24 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('padron', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='padron',
            name='carnetLibre',
        ),
        migrations.RemoveField(
            model_name='padron',
            name='carnetNoLibre',
        ),
        migrations.RemoveField(
            model_name='padron',
            name='genero',
        ),
    ]

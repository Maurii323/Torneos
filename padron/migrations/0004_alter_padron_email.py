# Generated by Django 5.0.4 on 2024-11-06 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('padron', '0003_alter_padron_nrodoc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='padron',
            name='email',
            field=models.CharField(max_length=45, unique=True),
        ),
    ]

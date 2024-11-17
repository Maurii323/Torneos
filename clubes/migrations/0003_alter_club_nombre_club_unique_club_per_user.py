# Generated by Django 5.1.3 on 2024-11-17 04:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubes', '0002_alter_club_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='nombre',
            field=models.CharField(max_length=45),
        ),
        migrations.AddConstraint(
            model_name='club',
            constraint=models.UniqueConstraint(fields=('user', 'nombre'), name='unique_club_per_user'),
        ),
    ]

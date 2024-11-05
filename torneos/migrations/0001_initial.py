# Generated by Django 5.0.4 on 2024-10-23 22:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clubes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Jornada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('juegosLocal', models.IntegerField(blank=True, null=True)),
                ('juegosVisitante', models.IntegerField(blank=True, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('jornada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torneos.jornada')),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_local', to='clubes.club')),
                ('visitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_visitante', to='clubes.club')),
            ],
        ),
        migrations.CreateModel(
            name='Torneo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fechaInicio', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='jornada',
            name='torneo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torneos.torneo'),
        ),
    ]
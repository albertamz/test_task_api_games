# Generated by Django 5.2.4 on 2025-07-13 11:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('result', models.CharField(choices=[('win', 'Win'), ('lose', 'Lose')], max_length=4)),
                ('prize', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('played_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_results', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

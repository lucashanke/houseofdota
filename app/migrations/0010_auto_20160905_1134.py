# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 11:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_heroesstatistics_counter_pick'),
    ]

    operations = [
        migrations.CreateModel(
            name='CounterStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero', models.IntegerField()),
                ('counter', models.IntegerField()),
                ('support', models.FloatField(default=0.0)),
                ('confidence_counter', models.FloatField(default=0.0)),
                ('confidence_hero', models.FloatField(default=0.0)),
                ('lift', models.FloatField(default=0.0)),
                ('patch_statistics', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='counter_statistics', to='app.PatchStatistics')),
            ],
        ),
        migrations.RemoveField(
            model_name='heroesstatistics',
            name='counter_pick',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-06 20:00
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_match_skill'),
    ]

    operations = [
        migrations.CreateModel(
            name='WinningBundleStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_bundle', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')])),
                ('bundle_size', models.IntegerField(default=1)),
                ('pick_rate', models.FloatField(default=0.0)),
                ('win_rate', models.FloatField(default=0.0)),
                ('frequency', models.FloatField(default=0.0)),
                ('patch_statistics', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='winning_bundles_statistics', to='app.PatchStatistics')),
            ],
        ),
    ]

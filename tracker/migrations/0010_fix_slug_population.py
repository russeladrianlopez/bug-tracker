# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-20 14:40
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_rename_team_to_teammember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name']),
        ),
    ]

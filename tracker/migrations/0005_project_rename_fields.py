# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-19 23:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_project_verbose_update'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='project_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='type_of_project',
            new_name='project_type',
        ),
    ]

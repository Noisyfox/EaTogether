# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 09:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ET', '0008_merge_20161025_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouporder',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ET.Courier'),
        ),
    ]

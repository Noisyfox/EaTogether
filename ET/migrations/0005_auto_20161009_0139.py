# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-08 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ET', '0004_auto_20161009_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='money',
            field=models.FloatField(default=0),
        ),
    ]

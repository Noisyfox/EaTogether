# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ET', '0011_auto_20161025_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalorder',
            name='status',
            field=models.CharField(choices=[('W', 'Waiting'), ('D', 'Delivering'), ('F', 'Delivered'), ('U', 'Undelivered')], default='W', max_length=1),
        ),
    ]
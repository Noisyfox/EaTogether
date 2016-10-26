# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 15:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ET', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='accept_time',
        ),
        migrations.RemoveField(
            model_name='group',
            name='confirm_delivery_time',
        ),
        migrations.RemoveField(
            model_name='group',
            name='delivery_start_time',
        ),
        migrations.AddField(
            model_name='grouporder',
            name='accept_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grouporder',
            name='confirm_delivery_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grouporder',
            name='delivery_start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grouporder',
            name='submit_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

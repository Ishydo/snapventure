# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snapventure', '0012_auto_20161110_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journey',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-21 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snapventure', '0018_auto_20161221_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journey',
            name='img_ambiance',
            field=models.ImageField(blank=True, default='uploads/img/default/journey-placeholder.png', upload_to='uploads/img/journey_ambiance'),
        ),
    ]

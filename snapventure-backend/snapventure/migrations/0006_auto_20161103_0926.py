# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-03 09:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snapventure', '0005_auto_20161103_0856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inscription',
            old_name='user',
            new_name='profile',
        ),
    ]
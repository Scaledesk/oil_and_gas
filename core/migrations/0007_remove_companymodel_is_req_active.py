# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 12:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20161115_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companymodel',
            name='is_req_active',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('sub_type', models.CharField(choices=[('BSC', 'Basic'), ('STD', 'Standard'), ('PRO', 'Pro'), ('PRE', 'Social Media')], max_length=3, primary_key=True, serialize=False)),
                ('cost_per_month', models.FloatField()),
                ('discount', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
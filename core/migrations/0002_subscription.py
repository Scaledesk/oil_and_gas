# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 06:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_type', models.CharField(choices=[('BSC', 'Basic'), ('STD', 'Standard'), ('PRO', 'Pro'), ('PRE', 'Social Media')], default='BSC', max_length=3)),
                ('sub_begin_time', models.DateField(default=None)),
                ('sub_end_time', models.DateField(default=None)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UserProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
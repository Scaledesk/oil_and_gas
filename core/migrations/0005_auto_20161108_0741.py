# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 07:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_brochure_certification_freefields_gallery_keyclient_location_premiumfields_sociallinks_subscription_'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyAlliance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='core.CompanyModel')),
                ('key_alliance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alliance', to='core.CompanyModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='keyclient',
            old_name='key_clients',
            new_name='key_client',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-04 00:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20170103_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='alt_phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-04 00:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20170103_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='alt_phone_number',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phone_number',
        ),
    ]

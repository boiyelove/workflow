# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-05 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20170104_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='lastpasswordreset',
            field=models.DateTimeField(null=True),
        ),
    ]

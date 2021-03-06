# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-07 20:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('published_on', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=160)),
                ('status', models.CharField(choices=[('Todo', 'Todo'), ('Doing', 'Doing'), ('Done', 'Done')], max_length=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('published_on', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=160)),
                ('status', models.CharField(choices=[('Todo', 'Todo'), ('Doing', 'Doing'), ('Done', 'Done')], max_length=5)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectflow.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

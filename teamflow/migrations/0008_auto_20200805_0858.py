# Generated by Django 3.1 on 2020-08-05 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamflow', '0007_auto_20170212_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaminvite',
            name='accepted',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='teaminvite',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
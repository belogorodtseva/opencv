# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-09 13:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('face_detector', '0002_photos_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

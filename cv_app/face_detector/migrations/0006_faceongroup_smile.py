# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-16 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_detector', '0005_auto_20180510_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='faceongroup',
            name='smile',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]

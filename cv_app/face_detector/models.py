# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Photos(models.Model):
    image = models.FileField(null=False)

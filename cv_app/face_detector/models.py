# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Photos(models.Model):
    image = models.FileField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

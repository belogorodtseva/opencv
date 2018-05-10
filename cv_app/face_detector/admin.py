# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from face_detector.models import *



admin.site.register(Emotion)
admin.site.register(FaceOnGroup)
admin.site.register(GroupPhoto)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Emotion(models.Model):
    sadness = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    neutral = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    contempt = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    disgust = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    anger = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    surprise = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    fear = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    happiness = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)


class HomePagePhoto(models.Model):
    image = models.FileField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class DiaryPhoto(models.Model):
    image = models.FileField(null=False)
    date = models.DateField(default=date.today)
    emotions = models.ForeignKey(Emotion, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class FramePhoto(models.Model):
    image = models.FileField(null=False)
    video = models.ForeignKey(Video, blank=False, null=False)


class Face(models.Model):
    gender = models.CharField(max_length=20, default='female', blank=False, null=False)
    emotions = models.ForeignKey(Emotion, blank=True, null=True)
    frame = models.ForeignKey(FramePhoto, blank=False, null=False)


class GroupPhoto(models.Model):
    image = models.FileField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class FaceOnGroup(models.Model):
    gender = models.CharField(max_length=20, default='female', blank=False, null=False)
    smile = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=False, null=False)
    emotions = models.ForeignKey(Emotion, blank=True, null=True)
    photo = models.ForeignKey(GroupPhoto, blank=False, null=False)

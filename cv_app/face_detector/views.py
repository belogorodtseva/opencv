# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import cv2
import sys
import os
from django.conf import settings
from django.shortcuts import render
from face_detector.models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from face_detector.forms import UploadFileForm
import datetime
from datetime import date
from datetime import datetime
import pytz
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
import numpy as np
import urllib
from urlparse import urlparse
from django.core.files import File
from numpy import array
import StringIO
import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from fusioncharts import FusionCharts

import matplotlib.pyplot as plt

from django.core.files.uploadedfile import InMemoryUploadedFile
from random import randint

from group import *
from video import *
from diary import *


########################## PAGES

### SING UP

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


### MAIN PAGE

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        result =  emotion_detect(request,uploaded_file_url)
        return render(request, 'mainpage.html', {
            'result': result
        })
    return render(request, 'mainpage.html')


### DIARY PAGE

@login_required(login_url='/login/')
def diary(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        photo = DiaryPhoto()
        photo.image = myfile
        user = User.objects.get(username=request.user.username)
        photo.user = user
        if request.POST['date']:
            photo.date = request.POST['date']
        photo.save()
        result =  diary_detect(request,uploaded_file_url,photo)
        line_plot=draw_line_plot(user)
        pie_plot=draw_pie_plot(user)
        return render(request, 'diary.html', {
            'result': result,
            'photo' : photo,
            'line_plot': line_plot.render(),
            'pie_plot': pie_plot.render(),
            'Diary' : DiaryPhoto.objects.filter(user=user)

        })
    else:
        user = User.objects.get(username=request.user.username)
        line_plot=draw_line_plot(user)
        pie_plot=draw_pie_plot(user)
        content = {
            'line_plot': line_plot.render(),
            'pie_plot': pie_plot.render(),
            'Diary' : DiaryPhoto.objects.filter(user=user)
        }
        return render(request, 'diary.html', content)


### GROUP PHOTO PAGE

@login_required(login_url='/login/')
def group(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        photo = GroupPhoto()
        photo.image = myfile
        user = User.objects.get(username=request.user.username)
        photo.user = user
        photo.save()
        result =  group_detect(request,uploaded_file_url,photo)
        if result !=666:
            line_r=line_result(photo)
            all_plot=draw_plots_all(photo)
            male_plot=draw_plots_male(photo)
            female_plot=draw_plots_female(photo)
            all_plot_smile=draw_plots_all_smile(photo)
            male_plot_smile=draw_plots_male_smile(photo)
            female_plot_smile=draw_plots_female_smile(photo)
            return render(request, 'group.html', {
                'result': result,
                'line_result': line_r,
                'photo' : photo,
                'all_plot': all_plot.render(),
                'male_plot': male_plot.render(),
                'female_plot': female_plot.render(),
                'all_plot_smile': all_plot_smile.render(),
                'male_plot_smile': male_plot_smile.render(),
                'female_plot_smile': female_plot_smile.render()
            })
        else:
            return render(request, 'group.html', {
                'result': result,
                'photo' : photo,
            })
    return render(request, 'group.html')


### VIDEO PAGE

@login_required(login_url='/login/')
def video(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        video = Video()
        video.user = User.objects.get(username=request.user.username)
        video.save()
        video_cut(uploaded_file_url,video)
        video_plot = draw_plot_video(video)
        video_plot_line = draw_line_video(video)
        frames = FramePhoto.objects.filter()
        result = 1
        smiles = show_smile(video)
        return render(request, 'video.html', {
            'filename': uploaded_file_url,
            'result': result,
            'video': video,
            'video_plot': video_plot.render(),
            'video_plot_line': video_plot_line.render(),
            'Frames' : FramePhoto.objects.filter(video=video),
            'smiles' : smiles,
        })
    return render(request, 'video.html')


### ABOUT PAGE

def about(request):
    content = {
    }
    return render(request, 'about.html', content)


### HISTORY PAGE

@login_required(login_url='/login/')
def history(request):

    content = {
        'Photos' : HomePagePhoto.objects.filter(user=User.objects.get(username=request.user.username))
    }
    return render(request, 'history.html', content)

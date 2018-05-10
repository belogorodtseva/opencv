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

import matplotlib.pyplot as plt

from django.core.files.uploadedfile import InMemoryUploadedFile

KEY = '2c88ec709ee943b49ac7c6202fad1a94'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

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
    content = {

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
        draw_plots(photo)
        return render(request, 'group.html', {
            'result': result,
            'photo' : photo,
            'faces' : FaceOnGroup.objects.filter(photo=photo)
        })
    return render(request, 'group.html')


### VIDEO PAGE

@login_required(login_url='/login/')
def video(request):
    content = {

    }
    return render(request, 'video.html', content)


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


########################## FUNCTIONS
def group_detect(request,img_url,photo):

    #emotionList = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']
    labels = 'sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness'
    url = img_url[1:]

    faces = CF.face.detect(url, face_id=True, landmarks=False, attributes='gender,emotion')
    faceCount = 0

    for face in faces:
        faceOnGroup = FaceOnGroup()
        faceOnGroup.photo = photo
        emotionOnGroup = Emotion()
        fa = face["faceAttributes"]
        emotion = fa["emotion"]
        faceOnGroup.gender = fa["gender"]
        emotions = []
        for e in emotion:
            emotions.append(emotion[e])
        emotionOnGroup.sadness = emotions[0]
        emotionOnGroup.neutral = emotions[1]
        emotionOnGroup.contempt = emotions[2]
        emotionOnGroup.disgust = emotions[3]
        emotionOnGroup.anger = emotions[4]
        emotionOnGroup.surprise = emotions[5]
        emotionOnGroup.fear = emotions[6]
        emotionOnGroup.happiness = emotions[7]
        emotionOnGroup.save()
        faceOnGroup.emotions = emotionOnGroup
        faceOnGroup.save()
        faceCount += 1


    sizes = emotions
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=80)
    ax1.axis('equal')

    plt.show()
    if faceCount == 0:
        return(666)
    else:
        return(faceCount)

def draw_plots(photo):
    emotionList = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']

    faces = FaceOnGroup.objects.filter(photo=photo)
    maleCounter = 0
    femaleCounter = 0
    maleArray = [ 0, 0 ,0, 0, 0, 0, 0, 0 ]
    femaleArray = [ 0, 0 ,0, 0, 0, 0, 0, 0 ]

    for face in faces:

        if face.gender == 'male':
            maleArray[best_emotion(face)] += 1
            maleCounter+=1
        else:
            femaleArray[best_emotion(face)] += 1
            femaleCounter+=1

    sizes = maleArray
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=emotionList, autopct='%1.1f%%',
                shadow=False,  startangle=90 )
    ax1.axis('equal')
    plt.title('Male result')
    plt.show()

    sizes = femaleArray
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=emotionList, autopct='%1.1f%%',
                shadow=False, startangle=80)
    ax1.axis('equal')
    plt.title('Female result')
    plt.show()



    sizes = maleArray
    #explsion
    explode = (0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05)
    colors = ['#2b5797', '#eff4ff', '#7e3878', '#00aba9', '#ffc40d', '#1e7145', '#99b433', '#ee1111']
    plt.pie(sizes, colors=colors, labels=emotionList, autopct='%1.1f%%', startangle=90, explode = explode)
    #draw circle
    centre_circle = plt.Circle((0,0),0.5,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')
    plt.tight_layout()
    plt.title('Male result')
    plt.show()

def best_emotion(face):

    emotionValues = [ face.emotions.sadness ,
                        face.emotions.neutral ,
                        face.emotions.contempt ,
                        face.emotions.disgust ,
                        face.emotions.anger ,
                        face.emotions.surprise ,
                        face.emotions.fear ,
                        face.emotions.happiness ]
    return(emotionValues.index(max(emotionValues)))



def detect(request, url):

    cascPath = "haarcascade_frontalface_default.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(url[1:])

    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)


    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces)>0:
        result = "Found {0} faces!".format(len(faces))
    else:
        result = 2

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 250, 0), 4)


    cv2.imwrite('media/new.png',image)
    img = Image.fromarray(image)



    newUrl=url[7:].split(".")
    nUrl=newUrl[0]+".png"
    tempfile_io =StringIO.StringIO()
    img.save(tempfile_io, format='PNG')
    image_file = InMemoryUploadedFile(tempfile_io, None, nUrl,'image/png',tempfile_io.len, None)


    if request.user.is_authenticated():
        photo = HomePagePhoto()
        photo.image = image_file
        user = User.objects.get(username=request.user.username)
        photo.user = user
        photo.save()


    return result


def emotion_detect(request,img_url):
    url="https://how-old.net/Images/faces2/main004.jpg"
    print(url)
    faces = CF.face.detect(url, face_id=True, landmarks=False, attributes='gender,emotion')
    fnt = ImageFont.truetype('Roboto-Bold.ttf', 15)
    #Download the image from the url
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    toShow=""
    #For each face returned use the face rectangle and draw a red box.
    draw = ImageDraw.Draw(img)
    for face in faces:
        draw.rectangle(getRectangle(face), outline='red')
        fa = face["faceAttributes"]
        emotion = fa["emotion"]
        for e in emotion:
            toShow+=e+"="+str(emotion[e])+"\n"

        print(toShow)
        draw.text(getEmotionLocation(face), toShow, font=fnt, fill='red')


    #Display the image in the users default image browser.
    img.show()
    print(faces)

    return(toShow)


#Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))


#Convert width height to a point in a rectangle
def getEmotionLocation(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']+10
    top = rect['top']+10
    return ((left, top))

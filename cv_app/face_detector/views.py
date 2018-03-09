# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import cv2
import sys
import os
from django.conf import settings
from django.shortcuts import render
from face_detector.models import Photos
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
from PIL import Image
from numpy import array
import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile




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


def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        result = detect(request,uploaded_file_url)
        return render(request, 'mainpage.html', {
            'result': result
        })
    return render(request, 'mainpage.html')

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
        scaleFactor=1.1,
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


    # Once you have a Django file-like object, you may assign it to your ImageField
    # and save.
    if request.user.is_authenticated():
        photo = Photos()
        photo.image = image_file
        user = User.objects.get(username=request.user.username)
        photo.user = user
        photo.save()


    return result



def about(request):
    content = {
    }
    return render(request, 'about.html', content)


@login_required(login_url='/login/')
def history(request):

    content = {

    }
    return render(request, 'history.html', content)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from face_detector.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404, get_object_or_404
import datetime
from datetime import date
from datetime import datetime
import pytz

from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect

from django.template import RequestContext
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


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
    content = {

    }
    return render(request, 'mainpage.html', content)



def about(request):
    content = {
    }
    return render(request, 'about.html', content)


@login_required(login_url='/login/')
def history(request):

    content = {

    }
    return render(request, 'history.html', content)

from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^history/', views.history, name='history'),
    url(r'^diary/', views.diary, name='diary'),
    url(r'^video/', views.video, name='video'),
    url(r'^group/', views.group, name='group'),
    ]

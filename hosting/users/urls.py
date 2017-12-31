# -*- coding: utf-8 -*-

from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
from users import views, admins

urlpatterns = [
    # App users paths
    path('dashboard', views.index),
    path('ftpmanager/', include('ftpmanager.urls')),
    path('domains/', include('domains.urls')),
    path('databases/', include('dbmanager.urls')),
    path('stats', views.stats),
    # Admin users paths
    path('appusers/', admins.views.appusers),
]
